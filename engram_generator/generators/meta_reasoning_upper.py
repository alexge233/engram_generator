"""Expanded generators for upper tiers 7-10.

Adds 9 more generators to bring the total to 247.
"""
from engram_generator.base import StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import register


# ── TIER 7 (15 → 18) ───────────────────────────────────────────────

@register
class VerifyProofGenerator(StepGenerator):
    """Verify if a given proof step is valid or contains an error."""

    @property
    def task_name(self) -> str:
        return "verify_proof"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["proof_by_induction", "error_detection"]

    def task_description(self, difficulty: int) -> str:
        return "verify proof step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "n^2 > 2n for n >= 3",
                "steps": ["base: 3^2=9 > 6=2*3", "assume k^2 > 2k",
                           "(k+1)^2 = k^2+2k+1 > 2k+2k+1 > 2(k+1)"],
                "valid": True, "reason": "all steps follow",
            },
            {
                "claim": "sum 1..n = n(n+1)/2",
                "steps": ["base: 1 = 1*2/2", "assume sum 1..k = k(k+1)/2",
                           "sum 1..k+1 = k(k+1)/2 + k+1 = (k+1)(k+2)/2"],
                "valid": True, "reason": "correct induction",
            },
            {
                "claim": "2^n > n^2 for n >= 1",
                "steps": ["base: 2^1=2 > 1=1^2", "assume 2^k > k^2",
                           "2^{k+1} = 2*2^k > 2k^2"],
                "valid": False, "reason": "2k^2 >= (k+1)^2 only for k>=3, base case fails at n=2",
            },
            {
                "claim": "all horses are the same colour",
                "steps": ["base: 1 horse trivially same colour",
                           "assume any k horses same colour",
                           "for k+1: first k same colour, last k same colour, overlap => all same"],
                "valid": False, "reason": "overlap is empty when k=1, induction step fails",
            },
            {
                "claim": "n! > 2^n for n >= 4",
                "steps": ["base: 4!=24 > 16=2^4", "assume k! > 2^k",
                           "(k+1)! = (k+1)*k! > (k+1)*2^k > 2*2^k = 2^{k+1} since k+1>=5>2"],
                "valid": True, "reason": "induction step valid for k>=4",
            },
            {
                "claim": "sum of first n odd numbers = n^2",
                "steps": ["base: 1 = 1^2", "assume 1+3+...+(2k-1) = k^2",
                           "add (2k+1): k^2 + 2k+1 = (k+1)^2"],
                "valid": True, "reason": "algebraic identity holds",
            },
            {
                "claim": "1/(1*2) + 1/(2*3) + ... + 1/(n*(n+1)) = n/(n+1)",
                "steps": ["base: 1/(1*2) = 1/2 = 1/(1+1)", "assume sum = k/(k+1)",
                           "add 1/((k+1)(k+2)): k/(k+1) + 1/((k+1)(k+2)) = (k(k+2)+1)/((k+1)(k+2)) = (k+1)^2/((k+1)(k+2)) = (k+1)/(k+2)"],
                "valid": True, "reason": "telescoping partial fractions",
            },
            {
                "claim": "every natural number > 1 is divisible by a prime",
                "steps": ["base: 2 is prime, divides itself",
                           "assume true for all 2..k-1",
                           "if k is prime, done; if k=ab with a,b<k, then a has a prime factor by hypothesis"],
                "valid": True, "reason": "strong induction, correct",
            },
            {
                "claim": "sqrt(n) is irrational for all n",
                "steps": ["assume sqrt(n) = a/b in lowest terms",
                           "n*b^2 = a^2, so n divides a^2, hence n divides a"],
                "valid": False, "reason": "fails for perfect squares: sqrt(4)=2 is rational",
            },
            {
                "claim": "if a|bc and gcd(a,b)=1 then a|c",
                "steps": ["gcd(a,b)=1 means ax+by=1 for some x,y",
                           "multiply by c: acx+bcy=c",
                           "a|acx trivially, a|bcy since a|bc, so a|c"],
                "valid": True, "reason": "Bezout's identity correctly applied",
            },
            {
                "claim": "derivative of x^n is nx^{n-1} for all n >= 1",
                "steps": ["base: d/dx(x) = 1 = 1*x^0", "assume d/dx(x^k) = kx^{k-1}",
                           "d/dx(x^{k+1}) = d/dx(x*x^k) = x^k + x*kx^{k-1} = x^k + kx^k = (k+1)x^k"],
                "valid": True, "reason": "product rule and induction correct",
            },
            {
                "claim": "2^n < n! for all n >= 1",
                "steps": ["base: 2^1=2 < 1!=1... wait, 2 > 1", "base case fails"],
                "valid": False, "reason": "base case is false: 2^1=2 > 1!=1",
            },
        ]
        idx = self._rng.randint(0, len(proofs) - 1)
        proof = proofs[idx]
        step_str = "; ".join(proof["steps"])
        problem = f"claim: {proof['claim']}; proof: {step_str}"
        return problem, proof

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"check: {s}" for s in sd["steps"]]

    def _create_answer(self, sd: dict) -> str:
        status = "VALID" if sd["valid"] else "INVALID"
        return f"{status}: {sd['reason']}"


@register
class DimensionalAnalysisGenerator(StepGenerator):
    """Check dimensional consistency of a physics formula."""

    @property
    def task_name(self) -> str:
        return "dimensional_analysis"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        return "check dimensional consistency"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        formulas = [
            {"formula": "v = d/t", "lhs": "m/s", "rhs": "m/s", "consistent": True},
            {"formula": "F = ma", "lhs": "kg*m/s^2", "rhs": "kg*m/s^2", "consistent": True},
            {"formula": "E = mc^2", "lhs": "kg*m^2/s^2", "rhs": "kg*(m/s)^2", "consistent": True},
            {"formula": "v = d*t", "lhs": "m/s", "rhs": "m*s", "consistent": False},
            {"formula": "F = m/a", "lhs": "kg*m/s^2", "rhs": "kg/(m/s^2)", "consistent": False},
            {"formula": "P = F*v", "lhs": "kg*m^2/s^3", "rhs": "kg*m/s^2*m/s", "consistent": True},
            {"formula": "W = F*d", "lhs": "kg*m^2/s^2", "rhs": "kg*m/s^2*m", "consistent": True},
            {"formula": "p = mv", "lhs": "kg*m/s", "rhs": "kg*m/s", "consistent": True},
            {"formula": "KE = mv^2", "lhs": "kg*m^2/s^2", "rhs": "kg*(m/s)^2", "consistent": False},
            {"formula": "T = 2*pi*sqrt(L/g)", "lhs": "s", "rhs": "sqrt(m/(m/s^2))=s", "consistent": True},
            {"formula": "PV = nRT", "lhs": "Pa*m^3", "rhs": "mol*(J/(mol*K))*K=J", "consistent": True},
            {"formula": "F = G*m1*m2/r", "lhs": "N", "rhs": "N*m (missing /r)", "consistent": False},
        ]
        f = self._rng.choice(formulas)
        problem = f"is {f['formula']} dimensionally consistent? LHS=[{f['lhs']}] RHS=[{f['rhs']}]"
        return problem, f

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"LHS: {sd['lhs']}", f"RHS: {sd['rhs']}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["consistent"] else "NO"


@register
class SymmetryDetectionGenerator(StepGenerator):
    """Detect if a function or expression has a symmetry property."""

    @property
    def task_name(self) -> str:
        return "symmetry_detection"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        return "detect symmetry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        sym_type = self._rng.choice(["even", "odd", "neither"])

        if sym_type == "even":
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^2 + {b}"
            reason = "f(-x) = f(x)"
        elif sym_type == "odd":
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^3 + {b}x"
            reason = "f(-x) = -f(x)"
        else:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^3 + {b}x^2 + {c}"
            reason = "f(-x) != f(x) and f(-x) != -f(x)"

        problem = f"classify symmetry: {func}"
        return problem, {"func": func, "type": sym_type, "reason": reason}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"compute f(-x)", sd["reason"]]

    def _create_answer(self, sd: dict) -> str:
        return sd["type"]


# ── TIER 8 (11 → 13) ───────────────────────────────────────────────

@register
class AbstractionLevelGenerator(StepGenerator):
    """Given a concrete problem, identify the abstract pattern."""

    @property
    def task_name(self) -> str:
        return "abstraction_level"

    @property
    def tier(self) -> int:
        return 8

    @property
    def prerequisites(self) -> list[str]:
        return ["isomorphism_detection"]

    def task_description(self, difficulty: int) -> str:
        return "identify abstract pattern"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        patterns = [
            {"concrete": "find shortest route between cities A and E through B,C,D",
             "abstract": "shortest path in weighted graph", "category": "graph_traversal"},
            {"concrete": "maximise profit given weight limit and item values",
             "abstract": "0/1 knapsack optimisation", "category": "dynamic_programming"},
            {"concrete": "find if a word can be built from magazine letter cutouts",
             "abstract": "multiset subset check", "category": "counting"},
            {"concrete": "schedule non-overlapping meetings to maximise attendance",
             "abstract": "interval scheduling maximisation", "category": "greedy"},
            {"concrete": "find the minimum number of coins to make change for amount N",
             "abstract": "minimum coin change (unbounded knapsack)", "category": "dynamic_programming"},
            {"concrete": "assign tasks to workers minimising total cost",
             "abstract": "assignment problem (bipartite matching)", "category": "graph_matching"},
            {"concrete": "determine if a jigsaw puzzle can be completed with given pieces",
             "abstract": "exact cover / constraint satisfaction", "category": "backtracking"},
            {"concrete": "rank web pages by importance based on link structure",
             "abstract": "eigenvector centrality (PageRank)", "category": "linear_algebra"},
            {"concrete": "find the longest common subsequence of two DNA strings",
             "abstract": "longest common subsequence", "category": "dynamic_programming"},
            {"concrete": "detect whether a social network has two opposing factions",
             "abstract": "bipartite graph check (2-coloring)", "category": "graph_theory"},
            {"concrete": "compress a file by finding repeated patterns",
             "abstract": "dictionary-based compression (LZ77/LZW)", "category": "information_theory"},
            {"concrete": "predict tomorrow's weather from today's using historical transitions",
             "abstract": "Markov chain state prediction", "category": "stochastic_process"},
        ]
        p = self._rng.choice(patterns)
        problem = f"abstractify: {p['concrete']}"
        return problem, p

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"concrete: {sd['concrete']}",
            f"pattern: {sd['abstract']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['abstract']} ({sd['category']})"


@register
class DualProblemGenerator(StepGenerator):
    """Given a problem, state its dual."""

    @property
    def task_name(self) -> str:
        return "dual_problem"

    @property
    def tier(self) -> int:
        return 8

    @property
    def prerequisites(self) -> list[str]:
        return ["problem_transformation"]

    def task_description(self, difficulty: int) -> str:
        return "state the dual problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        duals = [
            {"primal": "find minimum spanning tree", "dual": "find maximum weight cut", "domain": "graph theory"},
            {"primal": "minimise cost subject to constraints", "dual": "maximise lower bound from constraints", "domain": "linear programming"},
            {"primal": "find shortest path", "dual": "find maximum flow (by max-flow min-cut)", "domain": "network flow"},
            {"primal": "maximise entropy of a distribution", "dual": "minimise KL divergence from uniform", "domain": "information theory"},
            {"primal": "find minimum vertex cover", "dual": "find maximum independent set", "domain": "graph theory"},
            {"primal": "minimise error on training data", "dual": "maximise margin (SVM)", "domain": "machine learning"},
            {"primal": "find shortest tour visiting all cities", "dual": "find lower bound via LP relaxation", "domain": "combinatorial optimisation"},
            {"primal": "maximise likelihood", "dual": "minimise cross-entropy", "domain": "statistics"},
            {"primal": "find minimum cut", "dual": "find maximum flow", "domain": "network flow"},
            {"primal": "compress data (minimise bits)", "dual": "maximise information preserved", "domain": "information theory"},
            {"primal": "find densest subgraph", "dual": "find sparsest cut", "domain": "graph theory"},
            {"primal": "minimise total weighted completion time", "dual": "maximise schedule efficiency", "domain": "scheduling"},
        ]
        d = self._rng.choice(duals)
        problem = f"dual of: {d['primal']}"
        return problem, d

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"domain: {sd['domain']}", f"primal: {sd['primal']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["dual"]


# ── TIER 9 (11 → 13) ───────────────────────────────────────────────

@register
class InformationBottleneckGenerator(StepGenerator):
    """Identify what information a compression step loses."""

    @property
    def task_name(self) -> str:
        return "information_bottleneck"

    @property
    def tier(self) -> int:
        return 9

    @property
    def prerequisites(self) -> list[str]:
        return ["info_entropy", "complexity_comparison"]

    def task_description(self, difficulty: int) -> str:
        return "analyse information bottleneck"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {"operation": "mean pooling a sequence of embeddings",
             "preserves": "average magnitude and direction",
             "loses": "positional order, individual token identity"},
            {"operation": "PCA reducing 100D to 10D",
             "preserves": "top 10 variance components",
             "loses": "90 minor variance directions, possible nonlinear structure"},
            {"operation": "quantising fp32 weights to int8",
             "preserves": "approximate magnitude and sign",
             "loses": "precision within quantisation bins, outlier fidelity"},
            {"operation": "hashing a string to 32 bits",
             "preserves": "identity (with collision probability)",
             "loses": "content, length, structure, reversibility"},
            {"operation": "max pooling a 2D feature map with stride 2",
             "preserves": "strongest activation in each region",
             "loses": "spatial precision, weaker activations, exact position of max"},
            {"operation": "SVD truncating to rank k",
             "preserves": "best rank-k approximation in Frobenius norm",
             "loses": "n-k singular values and their associated structure"},
            {"operation": "downsampling audio from 44.1kHz to 8kHz",
             "preserves": "frequencies below 4kHz (Nyquist)",
             "loses": "all frequencies above 4kHz, audio fidelity"},
            {"operation": "converting RGB image to grayscale",
             "preserves": "luminance (weighted sum of channels)",
             "loses": "colour information, ability to distinguish same-brightness colours"},
            {"operation": "tokenising text with BPE (30K vocab)",
             "preserves": "most common subword patterns",
             "loses": "character-level granularity, rare character sequences split arbitrarily"},
            {"operation": "knowledge distillation from 70B to 7B model",
             "preserves": "soft label distribution on training data",
             "loses": "capacity for rare/complex patterns, tail distribution accuracy"},
            {"operation": "applying dropout with p=0.5",
             "preserves": "expected activation values (rescaled)",
             "loses": "co-adaptation between neurons, deterministic output"},
            {"operation": "replacing continuous actions with discrete buckets",
             "preserves": "approximate action selection",
             "loses": "fine-grained control, smoothness of policy"},
        ]
        s = self._rng.choice(scenarios)
        problem = f"what does '{s['operation']}' lose?"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"preserves: {sd['preserves']}", f"loses: {sd['loses']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["loses"]


@register
class ConvergenceProofGenerator(StepGenerator):
    """Determine if an iterative algorithm converges."""

    @property
    def task_name(self) -> str:
        return "convergence_proof"

    @property
    def tier(self) -> int:
        return 9

    @property
    def prerequisites(self) -> list[str]:
        return ["invariant_discovery", "learning_bound"]

    def task_description(self, difficulty: int) -> str:
        return "prove convergence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cases = [
            {"algorithm": "x_{n+1} = x_n/2", "converges": True, "limit": "0",
             "reason": "contraction mapping, ratio=0.5 < 1"},
            {"algorithm": "x_{n+1} = 2x_n", "converges": False, "limit": "diverges",
             "reason": "expansion, ratio=2 > 1"},
            {"algorithm": "x_{n+1} = (x_n + a/x_n)/2", "converges": True, "limit": "sqrt(a)",
             "reason": "Newton's method for sqrt, quadratic convergence"},
            {"algorithm": "x_{n+1} = cos(x_n)", "converges": True, "limit": "0.7391 (Dottie number)",
             "reason": "|cos'(x)| = |sin(x)| < 1 near fixed point"},
            {"algorithm": "x_{n+1} = x_n - f(x_n)/f'(x_n)", "converges": True, "limit": "root of f",
             "reason": "Newton-Raphson, quadratic convergence near simple roots"},
            {"algorithm": "x_{n+1} = 3.5*x_n*(1-x_n)", "converges": False, "limit": "chaotic",
             "reason": "logistic map with r=3.5 enters period-doubling chaos"},
            {"algorithm": "x_{n+1} = (x_n + 1/x_n)/2", "converges": True, "limit": "1",
             "reason": "AM-GM inequality: (x+1/x)/2 >= sqrt(x*1/x) = 1, decreasing for x>1"},
            {"algorithm": "a_{n+1} = sqrt(2 + a_n), a_0=0", "converges": True, "limit": "2",
             "reason": "bounded above by 2, monotonically increasing"},
            {"algorithm": "x_{n+1} = x_n^2", "converges": False, "limit": "diverges if |x_0|>1",
             "reason": "iterating squaring diverges unless |x_0|<=1"},
            {"algorithm": "SGD with fixed lr on convex loss", "converges": True, "limit": "neighbourhood of minimum",
             "reason": "convexity guarantees descent; fixed lr causes oscillation near minimum"},
            {"algorithm": "x_{n+1} = sin(x_n)", "converges": True, "limit": "0",
             "reason": "|sin(x)| < |x| for x != 0, so sequence contracts to 0"},
            {"algorithm": "power iteration: v_{n+1} = Av_n/||Av_n||", "converges": True,
             "limit": "dominant eigenvector", "reason": "converges if dominant eigenvalue is unique and real"},
        ]
        c = self._rng.choice(cases)
        problem = f"does {c['algorithm']} converge?"
        return problem, c

    def _create_steps(self, sd: dict) -> list[str]:
        return [sd["reason"]]

    def _create_answer(self, sd: dict) -> str:
        if sd["converges"]:
            return f"YES, limit={sd['limit']}"
        return "NO, diverges"


# ── TIER 10 (11 → 13) ──────────────────────────────────────────────

@register
class RegularisationDesignGenerator(StepGenerator):
    """Design a regularisation strategy for a stated overfitting problem."""

    @property
    def task_name(self) -> str:
        return "regularisation_design"

    @property
    def tier(self) -> int:
        return 10

    @property
    def prerequisites(self) -> list[str]:
        return ["loss_design", "training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        return "design regularisation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {"symptom": "train loss 0.01, val loss 2.5, 100M params on 10K samples",
             "diagnosis": "severe overfitting due to param/data ratio",
             "strategy": "L2 weight decay + dropout + data augmentation",
             "reason": "reduce effective capacity and increase data diversity"},
            {"symptom": "attention concentrating on single token for all inputs",
             "diagnosis": "attention collapse",
             "strategy": "attention entropy regularisation + multi-head diversity loss",
             "reason": "penalise low-entropy attention distributions"},
            {"symptom": "loss decreasing but generated text is repetitive",
             "diagnosis": "mode collapse in generation",
             "strategy": "nucleus sampling + repetition penalty + unlikelihood training",
             "reason": "diversify output distribution during both training and inference"},
            {"symptom": "validation accuracy plateaus at 60% while train reaches 99%",
             "diagnosis": "overfitting with insufficient generalisation",
             "strategy": "early stopping + mixup augmentation + label smoothing",
             "reason": "prevent memorisation and soften decision boundaries"},
            {"symptom": "loss spikes every few hundred steps then recovers",
             "diagnosis": "learning rate too high, unstable optimisation",
             "strategy": "reduce lr, add warmup, use gradient clipping",
             "reason": "stabilise gradient magnitudes and step sizes"},
            {"symptom": "all hidden representations collapse to similar vectors",
             "diagnosis": "representation collapse (dimensional collapse)",
             "strategy": "VICReg or Barlow Twins variance/covariance regularisation",
             "reason": "force dimensions to be informative and decorrelated"},
            {"symptom": "GAN generator produces same image regardless of input noise",
             "diagnosis": "mode collapse in GAN",
             "strategy": "minibatch discrimination + spectral normalisation",
             "reason": "force generator to produce diverse outputs"},
            {"symptom": "fine-tuned model forgets pre-trained capabilities",
             "diagnosis": "catastrophic forgetting",
             "strategy": "EWC (elastic weight consolidation) + low learning rate + replay buffer",
             "reason": "constrain weight changes important to previous tasks"},
            {"symptom": "embeddings of semantically different items have similar cosine similarity",
             "diagnosis": "anisotropic embedding space",
             "strategy": "contrastive loss + whitening + temperature scaling",
             "reason": "spread representations uniformly across the hypersphere"},
            {"symptom": "model confident on out-of-distribution inputs",
             "diagnosis": "poor calibration / overconfidence",
             "strategy": "temperature scaling + mixup + OOD detection head",
             "reason": "calibrate confidence to match actual accuracy"},
            {"symptom": "gradients vanish in early layers of deep network",
             "diagnosis": "vanishing gradients",
             "strategy": "residual connections + careful initialisation + batch normalisation",
             "reason": "ensure gradient signal reaches all layers"},
            {"symptom": "model size 10x larger than needed for task complexity",
             "diagnosis": "overparameterised for task",
             "strategy": "pruning + knowledge distillation + quantisation",
             "reason": "remove redundant parameters while preserving accuracy"},
        ]
        s = self._rng.choice(scenarios)
        problem = f"symptom: {s['symptom']}"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"diagnosis: {sd['diagnosis']}", f"reason: {sd['reason']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["strategy"]


@register
class BottleneckIdentificationGenerator(StepGenerator):
    """Identify the computational bottleneck in a model architecture."""

    @property
    def task_name(self) -> str:
        return "bottleneck_identification"

    @property
    def tier(self) -> int:
        return 10

    @property
    def prerequisites(self) -> list[str]:
        return ["efficiency_analysis", "architecture_analysis"]

    def task_description(self, difficulty: int) -> str:
        return "identify bottleneck"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {"arch": "transformer with seq_len=8192, d_model=512, 12 layers",
             "bottleneck": "self-attention (O(n^2) in seq_len)",
             "flops": "8192^2 * 512 * 12 = 412B per layer",
             "fix": "sparse attention, linear attention, or sliding window"},
            {"arch": "MLP with 1B params, batch_size=1",
             "bottleneck": "memory bandwidth (not compute-bound at batch 1)",
             "flops": "1B params * 2 = 2 GFLOPS, but 4GB memory transfer",
             "fix": "increase batch size to amortise memory transfer"},
            {"arch": "engram with 16 iterations, 8 layers per iteration",
             "bottleneck": "sequential iteration dependency (can't parallelise)",
             "flops": "16 * 8L forward = 128 layer passes",
             "fix": "reduce iterations via better halting, or wider per-iteration compute"},
            {"arch": "CNN with 50 layers, 3x3 kernels, no skip connections",
             "bottleneck": "vanishing gradients in deep stack",
             "flops": "moderate per-layer, but gradient signal dies",
             "fix": "add residual connections (ResNet)"},
            {"arch": "RNN processing sequence of length 10000",
             "bottleneck": "sequential dependency prevents parallelism",
             "flops": "10000 sequential steps, each O(d^2)",
             "fix": "replace with transformer or use chunked processing"},
            {"arch": "GAN with 512x512 output resolution",
             "bottleneck": "discriminator gradient signal at high resolution",
             "flops": "generator + discriminator per step",
             "fix": "progressive growing, multi-scale discriminator"},
            {"arch": "diffusion model with 1000 denoising steps",
             "bottleneck": "inference latency (1000 forward passes)",
             "flops": "1000 * model_forward",
             "fix": "DDIM (fewer steps), distillation, consistency models"},
            {"arch": "mixture of experts with 64 experts, top-2 routing",
             "bottleneck": "all-to-all communication for expert routing across GPUs",
             "flops": "2/64 of total params active per token, but routing overhead",
             "fix": "expert parallelism, reduce number of experts, local routing"},
            {"arch": "KV cache for 128K context window, d_model=4096",
             "bottleneck": "memory: 128K * 4096 * 2 * num_layers * 2 bytes per request",
             "flops": "attention itself is fast, but cache fills GPU memory",
             "fix": "GQA (grouped query attention), paged attention, quantised KV cache"},
            {"arch": "embedding table with 250K vocab, d_model=4096",
             "bottleneck": "softmax over 250K classes at output",
             "flops": "250K * d_model per token for final projection",
             "fix": "adaptive softmax, hierarchical softmax, or approximation"},
            {"arch": "ViT with 1024x1024 image patches of 16x16",
             "bottleneck": "4096 patches, attention is O(4096^2)",
             "flops": "16M attention entries per head per layer",
             "fix": "hierarchical patches (Swin), pooling, or linear attention"},
            {"arch": "autoregressive decoder generating 8192 tokens",
             "bottleneck": "sequential token generation (can't parallelise)",
             "flops": "8192 forward passes with growing KV cache",
             "fix": "speculative decoding, parallel decoding, or Medusa heads"},
        ]
        s = self._rng.choice(scenarios)
        problem = f"architecture: {s['arch']}"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"bottleneck: {sd['bottleneck']}", f"flops: {sd['flops']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['bottleneck']}; fix: {sd['fix']}"
