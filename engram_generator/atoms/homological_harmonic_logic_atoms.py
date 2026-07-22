"""Knowledge atoms for homological algebra, harmonic analysis, and mathematical logic."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── HOMOLOGICAL ALGEBRA (tier 7-8) ────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="chain_complex",
    content=(
        "A chain complex is a sequence of abelian groups or modules "
        "C_n connected by homomorphisms d_n: C_n -> C_{n-1} called "
        "boundary maps, satisfying d_{n-1} o d_n = 0 for all n. "
        "This means the image of each map is contained in the kernel "
        "of the next: im(d_n) subset ker(d_{n-1})."
    ),
    example=(
        "C: 0 -> Z --(x2)--> Z --(mod 2)--> Z/2Z -> 0. "
        "Check: (mod 2) o (x2)(n) = 2n mod 2 = 0. Valid chain complex."
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Chain complex', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chain_complex",
    prerequisites=["group_homomorphism"],
))

register_atom(Atom(
    atom_type="definition",
    name="homology_compute",
    content=(
        "The n-th homology group of a chain complex is H_n = ker(d_n) / im(d_{n+1}). "
        "It measures the failure of exactness: elements that are cycles "
        "(in ker d_n) but not boundaries (not in im d_{n+1})."
    ),
    example=(
        "C: 0 -> Z^2 --A--> Z^2 --B--> Z -> 0 with A=[[2,0],[0,3]], "
        "B=[1,1]. ker(B) = {(a,-a)} ~ Z. im(A) = {(2a,3b)}. "
        "H_1 = ker(B)/im(A) has generators from the quotient."
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Homology (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Homology_(mathematics)",
    prerequisites=["chain_complex"],
))

register_atom(Atom(
    atom_type="definition",
    name="exact_sequence",
    content=(
        "A sequence of groups and homomorphisms is exact at G_n if "
        "im(f_{n-1}) = ker(f_n). A short exact sequence is "
        "0 -> A -> B -> C -> 0, meaning f is injective, g is surjective, "
        "and im(f) = ker(g). Equivalently, C ~ B/A."
    ),
    example=(
        "0 -> Z --(x2)--> Z --(mod 2)--> Z/2Z -> 0. "
        "x2 is injective, mod 2 is surjective, im(x2) = 2Z = ker(mod 2). Exact."
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Exact sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Exact_sequence",
    prerequisites=["chain_complex"],
))

register_atom(Atom(
    atom_type="theorem",
    name="snake_lemma",
    content=(
        "Given a commutative diagram of two short exact sequences with "
        "vertical maps f, g, h, the snake lemma produces an exact sequence: "
        "0 -> ker(f) -> ker(g) -> ker(h) -d-> coker(f) -> coker(g) -> coker(h) -> 0, "
        "where d is the connecting homomorphism."
    ),
    example=(
        "Given 0->Z->Z^2->Z->0 with vertical maps (x2, x3, x6), "
        "ker(x2)=0, ker(x3)=0, ker(x6)=0, coker(x2)=Z/2Z, "
        "coker(x3)=Z/3Z, coker(x6)=Z/6Z. "
        "Snake: 0->0->0->0->Z/2Z->Z/3Z->Z/6Z->0."
    ),
    tier=8, domain="homological_algebra",
    source="Wikipedia contributors, 'Snake lemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Snake_lemma",
    prerequisites=["exact_sequence"],
))

register_atom(Atom(
    atom_type="definition",
    name="ext_functor",
    content=(
        "Ext^n(A, B) is the n-th right derived functor of Hom(A, -). "
        "Computed by taking a projective resolution of A, applying "
        "Hom(-, B), and taking cohomology. Ext^0(A, B) = Hom(A, B). "
        "Ext^1 classifies extensions of A by B."
    ),
    example=(
        "Ext^1(Z/2Z, Z): resolve Z/2Z by 0->Z--(x2)-->Z->Z/2Z->0. "
        "Apply Hom(-,Z): 0->Z--(x2)-->Z->0. "
        "H^1 = Z/2Z. So Ext^1(Z/2Z, Z) = Z/2Z."
    ),
    tier=8, domain="homological_algebra",
    source="Wikipedia contributors, 'Ext functor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ext_functor",
    prerequisites=["homology_compute", "exact_sequence"],
))

register_atom(Atom(
    atom_type="definition",
    name="tor_functor",
    content=(
        "Tor_n(A, B) is the n-th left derived functor of the tensor "
        "product A tensor -. Computed by taking a projective resolution "
        "of A, tensoring with B, and taking homology. "
        "Tor_0(A, B) = A tensor B. Tor measures the failure of "
        "flatness."
    ),
    example=(
        "Tor_1(Z/2Z, Z/3Z): resolve Z/2Z by 0->Z--(x2)-->Z->0. "
        "Tensor with Z/3Z: 0->Z/3Z--(x2)-->Z/3Z->0. "
        "ker(x2 on Z/3Z) = 0 (since gcd(2,3)=1). Tor_1 = 0."
    ),
    tier=8, domain="homological_algebra",
    source="Wikipedia contributors, 'Tor functor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tor_functor",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="free_resolution",
    content=(
        "A free resolution of a module M is an exact sequence "
        "... -> F_2 -> F_1 -> F_0 -> M -> 0 where each F_i is a "
        "free module. Every module over a PID has a free resolution "
        "of length at most 1."
    ),
    example=(
        "Free resolution of Z/6Z over Z: "
        "0 -> Z --(x6)--> Z -> Z/6Z -> 0. "
        "F_0 = Z (free), map is surjection, kernel = 6Z ~ Z = F_1."
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Free resolution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Free_resolution",
    prerequisites=["chain_complex"],
))

register_atom(Atom(
    atom_type="formula",
    name="euler_characteristic_chain",
    content=(
        "The Euler characteristic of a chain complex is "
        "chi = sum_{n} (-1)^n rank(C_n) = sum_{n} (-1)^n rank(H_n). "
        "This alternating sum is invariant under chain homotopy equivalence."
    ),
    example=(
        "Complex: 0 -> Z^3 -> Z^5 -> Z^2 -> 0. "
        "chi = 3 - 5 + 2 = 0. If H_0=Z, H_1=Z^2, H_2=0: "
        "check 0 - 2 + 1 = -1. (Values must match.)"
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Euler characteristic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euler_characteristic",
    prerequisites=["chain_complex", "homology_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="betti_number",
    content=(
        "The n-th Betti number b_n of a topological space X is the "
        "rank of its n-th homology group H_n(X; Z) modulo torsion. "
        "b_0 counts connected components, b_1 counts independent loops, "
        "b_2 counts enclosed cavities."
    ),
    example=(
        "Torus T^2: b_0=1 (connected), b_1=2 (two loops), b_2=1 (cavity). "
        "Euler characteristic = 1 - 2 + 1 = 0."
    ),
    tier=7, domain="homological_algebra",
    source="Wikipedia contributors, 'Betti number', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Betti_number",
    prerequisites=["homology_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="mayer_vietoris",
    content=(
        "The Mayer-Vietoris sequence relates the homology of a space X "
        "to the homology of two open subsets A, B with X = A union B: "
        "... -> H_n(A cap B) -> H_n(A) + H_n(B) -> H_n(X) -> H_{n-1}(A cap B) -> ..."
    ),
    example=(
        "S^1 = A union B where A, B are open arcs, A cap B = two points. "
        "H_0(two points) = Z^2, H_0(A)+H_0(B) = Z^2, H_0(S^1) = Z. "
        "Connecting map gives H_1(S^1) = Z."
    ),
    tier=8, domain="homological_algebra",
    source="Wikipedia contributors, 'Mayer-Vietoris sequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mayer%E2%80%93Vietoris_sequence",
    prerequisites=["exact_sequence", "homology_compute"],
))


# ── HARMONIC ANALYSIS (tier 5-7) ──────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="fourier_series_compute",
    content=(
        "The Fourier series of a periodic function f(x) with period 2L is "
        "f(x) = a_0/2 + sum_{n=1}^inf [a_n cos(n*pi*x/L) + b_n sin(n*pi*x/L)], "
        "where a_n = (1/L) integral_{-L}^{L} f(x)cos(n*pi*x/L)dx, "
        "b_n = (1/L) integral_{-L}^{L} f(x)sin(n*pi*x/L)dx."
    ),
    example=(
        "f(x) = x on [-pi, pi]: a_0=0 (odd function), a_n=0, "
        "b_n = (2/pi)*(-1)^{n+1}/n. "
        "f(x) = 2[sin(x) - sin(2x)/2 + sin(3x)/3 - ...]."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Fourier series', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Fourier_series",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="parseval_theorem",
    content=(
        "Parseval's theorem states that the total energy of a function "
        "equals the sum of energies of its Fourier components: "
        "(1/L) integral_{-L}^{L} |f(x)|^2 dx = "
        "|a_0|^2/2 + sum_{n=1}^inf (|a_n|^2 + |b_n|^2)."
    ),
    example=(
        "f(x) = x on [-pi, pi]: LHS = (1/pi)*integral_{-pi}^{pi} x^2 dx = 2*pi^2/3. "
        "RHS = sum 4/n^2 = 4 * pi^2/6 = 2*pi^2/3. Verified."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Parseval\\'s theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Parseval%27s_theorem",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="convolution_theorem",
    content=(
        "The Fourier transform of the convolution of two functions "
        "equals the product of their Fourier transforms: "
        "F{f * g} = F{f} . F{g}. Conversely, multiplication in the "
        "time domain corresponds to convolution in the frequency domain."
    ),
    example=(
        "f(t) = rect(t), g(t) = rect(t). F{rect} = sinc(w). "
        "F{f*g} = sinc^2(w). Inverse: (f*g)(t) = triangle(t)."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Convolution theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Convolution_theorem",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="windowed_fourier",
    content=(
        "The short-time Fourier transform (STFT) applies a window "
        "function w(t) before computing the Fourier transform: "
        "STFT{f}(tau, w) = integral f(t) * w(t - tau) * e^{-i*w*t} dt. "
        "This provides time-frequency localisation at the cost of "
        "resolution trade-off (uncertainty principle)."
    ),
    example=(
        "Gaussian window w(t) = e^{-t^2/2}, signal f(t) = cos(10t) for t<5, "
        "cos(20t) for t>=5. STFT shows frequency 10 before t=5, "
        "frequency 20 after t=5."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Short-time Fourier transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Short-time_Fourier_transform",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="wavelet_haar",
    content=(
        "The Haar wavelet is the simplest wavelet. The scaling function "
        "phi(t) = 1 for 0 <= t < 1, and the wavelet psi(t) = 1 for "
        "0 <= t < 1/2, -1 for 1/2 <= t < 1. Decomposition: "
        "approximation coefficient a = (x_0 + x_1)/2, "
        "detail coefficient d = (x_0 - x_1)/2."
    ),
    example=(
        "Signal [4, 6, 10, 2]: Level 1: a=[5, 6], d=[-1, 4]. "
        "Level 2: a=[5.5], d=[-0.5]. Coefficients: [5.5, -0.5, -1, 4]."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Haar wavelet', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Haar_wavelet",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="formula",
    name="spectral_density",
    content=(
        "The power spectral density (PSD) of a signal x(t) is "
        "S(f) = |X(f)|^2, where X(f) is the Fourier transform of x(t). "
        "By the Wiener-Khinchin theorem, S(f) is also the Fourier "
        "transform of the autocorrelation function R(tau)."
    ),
    example=(
        "White noise: R(tau) = sigma^2 * delta(tau). "
        "S(f) = sigma^2 (constant for all f). "
        "If sigma=2, S(f) = 4 for all frequencies."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Spectral density', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spectral_density",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="formula",
    name="laplace_inversion",
    content=(
        "The inverse Laplace transform recovers f(t) from F(s): "
        "f(t) = (1/2*pi*i) integral_{c-i*inf}^{c+i*inf} F(s)*e^{s*t} ds. "
        "In practice, partial fraction decomposition and lookup tables "
        "are used. L^{-1}{1/(s-a)} = e^{at}, L^{-1}{1/s^2} = t."
    ),
    example=(
        "F(s) = 3/(s-2) + 1/s^2. "
        "f(t) = 3*e^{2t} + t."
    ),
    tier=7, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Inverse Laplace transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inverse_Laplace_transform",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="hilbert_transform",
    content=(
        "The Hilbert transform of a function f(t) is "
        "H{f}(t) = (1/pi) PV integral_{-inf}^{inf} f(tau)/(t - tau) dtau, "
        "where PV denotes the Cauchy principal value. "
        "It produces a 90-degree phase shift of each frequency component."
    ),
    example=(
        "H{cos(wt)} = sin(wt), H{sin(wt)} = -cos(wt). "
        "For f(t) = cos(5t): H{f}(t) = sin(5t)."
    ),
    tier=7, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Hilbert transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hilbert_transform",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="sampling_reconstruction",
    content=(
        "The Nyquist-Shannon sampling theorem states that a band-limited "
        "signal with maximum frequency f_max can be perfectly reconstructed "
        "from samples taken at rate f_s >= 2*f_max (the Nyquist rate). "
        "Reconstruction uses sinc interpolation: "
        "x(t) = sum_n x[n] * sinc((t - n*T_s)/T_s)."
    ),
    example=(
        "Signal with f_max = 1000 Hz: Nyquist rate = 2000 Hz. "
        "Sampling at 2000 Hz (T_s = 0.5 ms) allows perfect reconstruction. "
        "Sampling at 1500 Hz causes aliasing."
    ),
    tier=5, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Nyquist-Shannon sampling theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem",
    prerequisites=["fourier_series_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="spectral_leakage",
    content=(
        "Spectral leakage occurs when a signal is not periodic within "
        "the analysis window. The DFT assumes periodicity, so a "
        "truncated signal produces side lobes in the spectrum that "
        "spread energy to adjacent frequency bins. Windowing functions "
        "(Hamming, Hanning, Blackman) reduce leakage by tapering the "
        "signal edges to zero."
    ),
    example=(
        "Sine wave at 10.5 Hz sampled at 100 Hz with N=100 (1 sec): "
        "not an integer number of cycles. DFT shows energy spread "
        "across bins 10 and 11 instead of a single peak. "
        "Hanning window concentrates energy near bin 10.5."
    ),
    tier=6, domain="harmonic_analysis",
    source="Wikipedia contributors, 'Spectral leakage', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Spectral_leakage",
    prerequisites=["fourier_series_compute", "sampling_reconstruction"],
))


# ── MATHEMATICAL LOGIC (tier 6-8) ─────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="first_order_satisfaction",
    content=(
        "A first-order structure M satisfies a sentence phi (M |= phi) "
        "if phi is true when its quantifiers range over the domain of M, "
        "its relation symbols are interpreted by M's relations, and its "
        "function symbols by M's functions. This defines the semantics "
        "of first-order logic."
    ),
    example=(
        "Structure M = (N, <). Sentence: forall x exists y (x < y). "
        "True in M because for any natural number n, n < n+1. "
        "So M |= forall x exists y (x < y)."
    ),
    tier=6, domain="mathematical_logic",
    source="Wikipedia contributors, 'First-order logic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/First-order_logic",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="prenex_normal_form",
    content=(
        "A formula is in prenex normal form (PNF) when it consists of "
        "a string of quantifiers (the prefix) followed by a quantifier-free "
        "formula (the matrix): Q_1 x_1 ... Q_n x_n phi(x_1,...,x_n). "
        "Every first-order formula has an equivalent PNF, obtained by "
        "moving quantifiers outward using equivalences like "
        "not(forall x phi) = exists x (not phi)."
    ),
    example=(
        "Formula: (forall x P(x)) -> (exists y Q(y)). "
        "Step 1: not(forall x P(x)) v (exists y Q(y)). "
        "Step 2: (exists x not P(x)) v (exists y Q(y)). "
        "PNF: exists x exists y (not P(x) v Q(y))."
    ),
    tier=6, domain="mathematical_logic",
    source="Wikipedia contributors, 'Prenex normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Prenex_normal_form",
    prerequisites=["first_order_satisfaction"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="skolemisation",
    content=(
        "Skolemisation removes existential quantifiers from a prenex "
        "formula by replacing each existentially quantified variable "
        "with a Skolem function of the preceding universally quantified "
        "variables. The result is equisatisfiable (not equivalent) to "
        "the original."
    ),
    example=(
        "forall x exists y R(x, y). "
        "Skolemise: replace y with f(x). "
        "Result: forall x R(x, f(x)), where f is a new function symbol."
    ),
    tier=7, domain="mathematical_logic",
    source="Wikipedia contributors, 'Skolem normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Skolem_normal_form",
    prerequisites=["prenex_normal_form"],
))

register_atom(Atom(
    atom_type="definition",
    name="herbrand_universe",
    content=(
        "The Herbrand universe of a set of clauses is the set of all "
        "ground terms that can be formed from the constants and function "
        "symbols in the clauses. If no constants exist, a fresh constant "
        "is added. The Herbrand base is the set of all ground atoms "
        "over the Herbrand universe."
    ),
    example=(
        "Clauses: P(a, f(x)). Constants: {a}. Functions: {f}. "
        "Herbrand universe: {a, f(a), f(f(a)), ...}. "
        "Depth 0: {a}. Depth 1: {a, f(a)}. Depth 2: {a, f(a), f(f(a))}."
    ),
    tier=7, domain="mathematical_logic",
    source="Wikipedia contributors, 'Herbrand structure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Herbrand_structure",
    prerequisites=["skolemisation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="tableau_proof",
    content=(
        "An analytic tableau (truth tree) is a proof method that "
        "systematically decomposes formulas. To prove phi, assume "
        "not phi and decompose using branching rules. If every branch "
        "closes (contains both A and not A), then phi is a theorem. "
        "Alpha rules don't branch (conjunctions); beta rules branch "
        "(disjunctions)."
    ),
    example=(
        "Prove p -> (p v q). Negate: p ^ not(p v q). "
        "Decompose: p, not p, not q. Branch contains p and not p. "
        "Closed. Therefore p -> (p v q) is valid."
    ),
    tier=7, domain="mathematical_logic",
    source="Wikipedia contributors, 'Method of analytic tableaux', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Method_of_analytic_tableaux",
    prerequisites=["prenex_normal_form"],
))

register_atom(Atom(
    atom_type="theorem",
    name="craig_interpolation",
    content=(
        "Craig's interpolation theorem: if phi |= psi (phi entails psi), "
        "then there exists a formula theta (the interpolant) such that "
        "phi |= theta and theta |= psi, where theta uses only non-logical "
        "symbols common to both phi and psi."
    ),
    example=(
        "phi = P(a) ^ Q(b), psi = P(a) v R(c). "
        "phi |= psi since P(a) holds. "
        "Interpolant: theta = P(a) (uses only P, a which appear in both). "
        "phi |= P(a) and P(a) |= P(a) v R(c)."
    ),
    tier=8, domain="mathematical_logic",
    source="Wikipedia contributors, 'Craig interpolation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Craig_interpolation",
    prerequisites=["first_order_satisfaction"],
))

register_atom(Atom(
    atom_type="definition",
    name="temporal_logic",
    content=(
        "Linear temporal logic (LTL) extends propositional logic with "
        "temporal operators: G (globally/always), F (finally/eventually), "
        "X (next), U (until). G phi means phi holds at every future state. "
        "F phi means phi holds at some future state. phi U psi means "
        "phi holds until psi becomes true."
    ),
    example=(
        "Trace: [p, p, p^q, q, q]. "
        "G p? No (p fails at state 4). "
        "F q? Yes (q holds at state 3). "
        "p U q? Yes (p holds at states 1-3, q holds at state 3)."
    ),
    tier=7, domain="mathematical_logic",
    source="Wikipedia contributors, 'Linear temporal logic', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Linear_temporal_logic",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="satisfiability_check",
    content=(
        "Boolean satisfiability (SAT) asks whether a propositional "
        "formula has a satisfying assignment. For CNF formulas, "
        "the DPLL algorithm uses unit propagation, pure literal "
        "elimination, and backtracking search. SAT is NP-complete "
        "but modern solvers handle millions of variables."
    ),
    example=(
        "CNF: (p v q) ^ (not p v r) ^ (not q v not r). "
        "Try p=T: (T) ^ (F v r) ^ (not q v not r). "
        "Need r=T: (T) ^ (T) ^ (not q v F). "
        "Need not q: q=F. Assignment: p=T, q=F, r=T. SAT."
    ),
    tier=6, domain="mathematical_logic",
    source="Wikipedia contributors, 'Boolean satisfiability problem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Boolean_satisfiability_problem",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="clause_resolution",
    content=(
        "Resolution is a rule of inference for propositional and "
        "first-order logic. Given clauses C1 = {A, ...} and "
        "C2 = {not A, ...}, the resolvent is (C1 - {A}) union (C2 - {not A}). "
        "Resolution is refutation-complete: a set of clauses is "
        "unsatisfiable iff the empty clause can be derived."
    ),
    example=(
        "Clauses: {p, q}, {not p, r}, {not q}, {not r}. "
        "Resolve {p, q} with {not p, r}: {q, r}. "
        "Resolve {q, r} with {not q}: {r}. "
        "Resolve {r} with {not r}: {} (empty clause). Unsatisfiable."
    ),
    tier=6, domain="mathematical_logic",
    source="Wikipedia contributors, 'Resolution (logic)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Resolution_(logic)",
    prerequisites=["satisfiability_check"],
))

register_atom(Atom(
    atom_type="theorem",
    name="godel_incompleteness",
    content=(
        "Goedel's first incompleteness theorem: any consistent formal "
        "system F capable of expressing basic arithmetic contains "
        "statements that are true but unprovable within F. "
        "The second theorem: F cannot prove its own consistency, "
        "assuming F is consistent."
    ),
    example=(
        "The Goedel sentence G for system F states 'G is not provable "
        "in F'. If F is consistent, G is true but unprovable. "
        "If G were provable, F would prove a falsehood, contradicting "
        "consistency."
    ),
    tier=8, domain="mathematical_logic",
    source="Wikipedia contributors, 'Goedel\\'s incompleteness theorems', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems",
    prerequisites=["first_order_satisfaction"],
))
