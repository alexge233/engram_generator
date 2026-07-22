"""Knowledge atoms for algorithm patterns, algebraic geometry, and particle physics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Algorithm patterns (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="theorem",
    name="divide_conquer_recurrence",
    content=(
        "The Master Theorem provides a direct solution for recurrences of the "
        "form T(n) = aT(n/b) + f(n), where a >= 1 and b > 1. There are three "
        "cases depending on how f(n) compares to n^(log_b a): Case 1: if "
        "f(n) = O(n^(log_b a - e)) then T(n) = Theta(n^(log_b a)); Case 2: "
        "if f(n) = Theta(n^(log_b a)) then T(n) = Theta(n^(log_b a) log n); "
        "Case 3: if f(n) = Omega(n^(log_b a + e)) then T(n) = Theta(f(n))."
    ),
    tier=5,
    domain="algorithms",
    example=(
        "Merge sort: T(n) = 2T(n/2) + O(n). a=2, b=2, log_b(a)=1, "
        "f(n) = n = Theta(n^1). Case 2 applies: T(n) = Theta(n log n)."
    ),
    source="Wikipedia contributors, 'Master theorem (analysis of algorithms)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)",
    prerequisites=["exponentiation", "logarithm"],
))

register_atom(Atom(
    atom_type="definition",
    name="amortised_analysis",
    content=(
        "Amortised analysis determines the average time per operation over a "
        "worst-case sequence of operations. Three methods: aggregate analysis "
        "(total cost / n operations), the accounting method (assign amortised "
        "costs, store credit for cheap operations), and the potential method "
        "(define a potential function Phi, amortised cost = actual cost + "
        "delta Phi). The amortised cost is an upper bound on the average "
        "per-operation cost."
    ),
    tier=6,
    domain="algorithms",
    example=(
        "Dynamic array doubling: n insertions cost at most 3n total. "
        "Amortised cost = 3n/n = O(1) per insertion, even though some "
        "individual insertions cost O(n) for copying."
    ),
    source="Wikipedia contributors, 'Amortized analysis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Amortized_analysis",
    prerequisites=["divide_conquer_recurrence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="greedy_proof",
    content=(
        "A greedy algorithm makes the locally optimal choice at each step. "
        "To prove correctness, two properties suffice: (1) Greedy choice "
        "property: a globally optimal solution can be arrived at by making "
        "a locally optimal (greedy) choice. (2) Optimal substructure: an "
        "optimal solution contains optimal solutions to its subproblems. "
        "The exchange argument is a common proof technique: assume an optimal "
        "solution differs from the greedy solution, then show the greedy "
        "choice can be substituted without worsening the solution."
    ),
    tier=7,
    domain="algorithms",
    example=(
        "Activity selection: activities sorted by finish time. Greedy picks "
        "earliest finish. Given {(1,3),(2,5),(4,7),(6,9)}: pick (1,3), skip "
        "(2,5), pick (4,7), skip (6,9). Result: 2 activities (optimal)."
    ),
    source="Wikipedia contributors, 'Greedy algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Greedy_algorithm",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="definition",
    name="dp_optimal_substructure",
    content=(
        "Dynamic programming applies when a problem has optimal substructure "
        "(an optimal solution contains optimal solutions to subproblems) and "
        "overlapping subproblems (the same subproblems are solved repeatedly). "
        "The Bellman equation formalises this: the value of a state equals "
        "the optimal choice among transitions plus the value of the resulting "
        "state. Solutions use either top-down memoisation or bottom-up "
        "tabulation."
    ),
    tier=6,
    domain="algorithms",
    example=(
        "Fibonacci via DP: F(n) = F(n-1) + F(n-2). Bottom-up: "
        "F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5. "
        "O(n) time vs O(2^n) naive recursion."
    ),
    source="Wikipedia contributors, 'Dynamic programming', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dynamic_programming",
    prerequisites=["fibonacci"],
))

register_atom(Atom(
    atom_type="theorem",
    name="np_reduction",
    content=(
        "A polynomial-time reduction from problem A to problem B (A <=_p B) "
        "is a polynomial-time computable function f such that x in A iff "
        "f(x) in B. If B is in P and A <=_p B, then A is in P. A problem "
        "is NP-hard if every problem in NP reduces to it in polynomial time. "
        "A problem is NP-complete if it is both in NP and NP-hard. The "
        "Cook-Levin theorem shows SAT is NP-complete."
    ),
    tier=7,
    domain="algorithms",
    example=(
        "3-SAT <=_p CLIQUE: given a 3-SAT formula with k clauses, construct "
        "a graph with 3k nodes (one per literal per clause). Add edges "
        "between non-contradictory literals in different clauses. The formula "
        "is satisfiable iff the graph has a k-clique."
    ),
    source="Wikipedia contributors, 'NP-completeness', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/NP-completeness",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="definition",
    name="approximation_ratio",
    content=(
        "An approximation algorithm for an optimisation problem has "
        "approximation ratio rho(n) if for every input of size n, the cost "
        "C of the approximate solution satisfies C/C* <= rho(n) for "
        "minimisation (or C*/C <= rho(n) for maximisation), where C* is the "
        "optimal cost. A polynomial-time approximation scheme (PTAS) achieves "
        "ratio 1+epsilon for any epsilon > 0."
    ),
    tier=6,
    domain="algorithms",
    example=(
        "Vertex cover 2-approximation: take both endpoints of each edge in "
        "a maximal matching. For K4: maximal matching {(1,2),(3,4)}, cover = "
        "{1,2,3,4} size 4. Optimal cover size >= 2 (matching size). "
        "Ratio = 4/2 = 2."
    ),
    source="Wikipedia contributors, 'Approximation algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Approximation_algorithm",
    prerequisites=["np_reduction"],
))

register_atom(Atom(
    atom_type="definition",
    name="randomised_algorithm",
    content=(
        "A randomised algorithm uses random bits to guide computation. "
        "Las Vegas algorithms always produce correct results but have "
        "random running time (e.g., randomised quicksort, expected O(n log n)). "
        "Monte Carlo algorithms have deterministic running time but may "
        "produce incorrect results with bounded probability (e.g., "
        "Miller-Rabin primality test). The expected complexity is analysed "
        "over the random choices."
    ),
    tier=6,
    domain="algorithms",
    example=(
        "Randomised quicksort: pick a random pivot. Expected comparisons = "
        "2n*H_n ~ 2n*ln(n). For n=100: ~2*100*4.605 = 921 comparisons "
        "expected vs O(n^2) = 10000 worst case with fixed pivot."
    ),
    source="Wikipedia contributors, 'Randomized algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Randomized_algorithm",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="definition",
    name="online_algorithm",
    content=(
        "An online algorithm processes input sequentially without knowledge "
        "of future elements. The competitive ratio measures performance "
        "against an optimal offline algorithm: ratio = max(cost_online / "
        "cost_offline) over all inputs. A c-competitive algorithm has "
        "cost_online <= c * cost_offline + alpha for some constant alpha. "
        "The ski rental problem and paging are classic examples."
    ),
    tier=7,
    domain="algorithms",
    example=(
        "Ski rental: rent costs $1/day, buying costs $b. Optimal online: "
        "rent for b-1 days, then buy. Competitive ratio = (b-1+b)/b = "
        "(2b-1)/b < 2. For b=10: rent 9 days ($9) then buy ($10) = $19 "
        "vs optimal $10. Ratio = 19/10 = 1.9."
    ),
    source="Wikipedia contributors, 'Online algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Online_algorithm",
    prerequisites=["amortised_analysis"],
))


# ---------------------------------------------------------------------------
# Algebraic geometry (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="variety_points",
    content=(
        "An algebraic variety is the set of solutions to a system of "
        "polynomial equations over a field. An affine variety V(I) in A^n "
        "is the zero locus of an ideal I in k[x_1,...,x_n]. Points on "
        "the variety satisfy all polynomials in the ideal simultaneously. "
        "The Zariski topology defines closed sets as varieties."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "V(x^2 + y^2 - 1) over R: the unit circle. Points: (1,0), (0,1), "
        "(-1,0), (0,-1), (3/5, 4/5), etc. Over F_5: (1,0), (4,0), (0,1), "
        "(0,4), (2,1), (2,4), (3,1), (3,4) -- 8 points."
    ),
    source="Wikipedia contributors, 'Algebraic variety', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Algebraic_variety",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="ideal_membership",
    content=(
        "The ideal membership problem asks whether a polynomial f belongs "
        "to an ideal I = <g_1,...,g_k>. This is solved using Groebner "
        "bases: compute the Groebner basis G of I, then divide f by G. "
        "f is in I iff the remainder is zero. Buchberger's algorithm "
        "computes the Groebner basis by iteratively adding S-polynomial "
        "remainders until no new elements are generated."
    ),
    tier=7,
    domain="algebraic_geometry",
    example=(
        "Is x^2 + y in <x + y, x - y>? Groebner basis (lex order): "
        "{x + y, 2y}. Divide x^2 + y: x^2 + y -> x(x+y) - xy + y "
        "-> -xy + y -> -y(x+y) + y^2 + y -> y^2 + y -> y(2y)/2 + y/2. "
        "Remainder 0 if char != 2, so yes."
    ),
    source="Wikipedia contributors, 'Groebner basis', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gr%C3%B6bner_basis",
    prerequisites=["polynomial_ring"],
))

register_atom(Atom(
    atom_type="theorem",
    name="bezout_intersection",
    content=(
        "Bezout's theorem states that two projective plane curves of "
        "degrees m and n, defined over an algebraically closed field and "
        "having no common component, intersect in exactly m*n points "
        "counted with multiplicity. This is a fundamental result in "
        "algebraic geometry connecting degree to intersection number."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "Line (degree 1) meets conic (degree 2): 1*2 = 2 intersection "
        "points. y = x meets x^2 + y^2 = 2: x^2 + x^2 = 2, x = +/-1. "
        "Points: (1,1) and (-1,-1). Count = 2 = 1*2."
    ),
    source="Wikipedia contributors, 'Bezout's theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/B%C3%A9zout%27s_theorem",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="elliptic_curve_group_law",
    content=(
        "An elliptic curve E: y^2 = x^3 + ax + b (with 4a^3 + 27b^2 != 0) "
        "forms an abelian group under the chord-tangent law. To add points "
        "P and Q: draw the line through P and Q, find the third intersection "
        "R with E, then P + Q = -R (reflect over the x-axis). The point "
        "at infinity O serves as the identity element."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "E: y^2 = x^3 - 7x + 10. P=(1,2), Q=(3,4). Slope m = (4-2)/(3-1) "
        "= 1. x_R = m^2 - x_P - x_Q = 1 - 1 - 3 = -3. y_R = m(x_P - x_R) "
        "- y_P = 1(1-(-3)) - 2 = 2. P+Q = (-3, -2)."
    ),
    source="Wikipedia contributors, 'Elliptic curve', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Elliptic_curve",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="projective_coords",
    content=(
        "Projective space P^n over a field k is the set of equivalence "
        "classes of (n+1)-tuples [x_0:x_1:...:x_n] where (x_0,...,x_n) != 0 "
        "and [x_0:...:x_n] = [lambda*x_0:...:lambda*x_n] for any nonzero "
        "lambda. Affine space embeds via (x_1,...,x_n) -> [1:x_1:...:x_n]. "
        "Points at infinity have x_0 = 0."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "P^1 over R: points [1:t] for t in R plus [0:1] (point at infinity). "
        "[2:6] = [1:3] (same equivalence class). The affine point x=3 "
        "maps to [1:3]."
    ),
    source="Wikipedia contributors, 'Projective space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Projective_space",
    prerequisites=["change_of_basis"],
))

register_atom(Atom(
    atom_type="definition",
    name="genus_compute",
    content=(
        "The geometric genus g of a smooth projective curve of degree d "
        "in P^2 is given by the degree-genus formula: g = (d-1)(d-2)/2. "
        "For a curve with delta ordinary double points, the arithmetic "
        "genus is g_a = (d-1)(d-2)/2 - delta. The genus determines the "
        "topology of the curve (number of handles of the Riemann surface)."
    ),
    tier=7,
    domain="algebraic_geometry",
    example=(
        "Smooth cubic (d=3): g = (3-1)(3-2)/2 = 2*1/2 = 1 (elliptic curve). "
        "Smooth quartic (d=4): g = (4-1)(4-2)/2 = 3*2/2 = 3. "
        "Line (d=1): g = 0. Conic (d=2): g = 0."
    ),
    source="Wikipedia contributors, 'Genus (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Genus_(mathematics)",
    prerequisites=["bezout_intersection"],
))

register_atom(Atom(
    atom_type="definition",
    name="rational_points",
    content=(
        "A rational point on a variety V defined over Q is a point whose "
        "coordinates are all rational numbers. For elliptic curves over Q, "
        "the Mordell-Weil theorem states that the group of rational points "
        "E(Q) is finitely generated: E(Q) ~ Z^r x T where r is the rank "
        "and T is the torsion subgroup. Finding rational points is central "
        "to Diophantine geometry."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "x^2 + y^2 = 1 over Q: rational points include (3/5, 4/5), "
        "(5/13, 12/13), (0, 1), (1, 0). Parametrised by "
        "x = (1-t^2)/(1+t^2), y = 2t/(1+t^2) for t in Q."
    ),
    source="Wikipedia contributors, 'Rational point', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rational_point",
    prerequisites=["elliptic_curve_group_law"],
))

register_atom(Atom(
    atom_type="definition",
    name="tangent_line_variety",
    content=(
        "The tangent line to a plane curve f(x,y) = 0 at a smooth point "
        "(a,b) is given by f_x(a,b)(x-a) + f_y(a,b)(y-b) = 0, where "
        "f_x and f_y are partial derivatives. A point is singular if both "
        "partial derivatives vanish there. For a projective curve, the "
        "tangent is defined analogously using the homogeneous gradient."
    ),
    tier=6,
    domain="algebraic_geometry",
    example=(
        "Curve x^2 + y^2 = 25 at point (3,4): f_x = 2x = 6, f_y = 2y = 8. "
        "Tangent: 6(x-3) + 8(y-4) = 0, i.e., 6x + 8y = 50, "
        "or 3x + 4y = 25."
    ),
    source="Wikipedia contributors, 'Tangent', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tangent",
    prerequisites=["derivative"],
))


# ---------------------------------------------------------------------------
# Particle physics (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="conservation_laws",
    content=(
        "In particle physics, several quantities are conserved in all "
        "interactions: energy, momentum, electric charge, baryon number, "
        "and lepton number. Additional quantities are conserved in specific "
        "interactions: strangeness, charm, bottomness, and topness are "
        "conserved in strong and electromagnetic interactions but may be "
        "violated in weak interactions. Conservation laws arise from "
        "symmetries via Noether's theorem."
    ),
    tier=5,
    domain="particle_physics",
    example=(
        "Neutron decay: n -> p + e- + nu_e_bar. Charge: 0 -> +1 + (-1) + 0 "
        "= 0 (conserved). Baryon number: 1 -> 1 + 0 + 0 = 1 (conserved). "
        "Lepton number: 0 -> 0 + 1 + (-1) = 0 (conserved)."
    ),
    source="Wikipedia contributors, 'Conservation law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conservation_law",
    prerequisites=["addition"],
))

register_atom(Atom(
    atom_type="definition",
    name="quark_content",
    content=(
        "Hadrons are composite particles made of quarks. Baryons contain "
        "three quarks (e.g., proton = uud, neutron = udd). Mesons contain "
        "a quark-antiquark pair (e.g., pi+ = u d_bar). The six quark "
        "flavours are: up (u, charge +2/3), down (d, -1/3), charm (c, +2/3), "
        "strange (s, -1/3), top (t, +2/3), bottom (b, -1/3)."
    ),
    tier=5,
    domain="particle_physics",
    example=(
        "Proton = uud: charge = 2/3 + 2/3 + (-1/3) = +1. "
        "Sigma+ = uus: charge = 2/3 + 2/3 + (-1/3) = +1, strangeness = -1. "
        "K+ = u s_bar: charge = 2/3 + 1/3 = +1, strangeness = +1."
    ),
    source="Wikipedia contributors, 'Quark model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quark_model",
    prerequisites=["conservation_laws"],
))

register_atom(Atom(
    atom_type="definition",
    name="feynman_vertex",
    content=(
        "A Feynman diagram vertex represents an interaction between "
        "particles. Each vertex has an associated coupling constant. "
        "In QED, the fundamental vertex couples an electron, a positron, "
        "and a photon with coupling sqrt(alpha) ~ e. The vertex factor "
        "is -ie*gamma^mu. Conservation of charge, energy, and momentum "
        "applies at each vertex."
    ),
    tier=6,
    domain="particle_physics",
    example=(
        "QED vertex: e- -> e- + gamma (electron emits photon). "
        "Coupling = sqrt(alpha) ~ sqrt(1/137) ~ 0.0854. "
        "Each vertex contributes factor sqrt(alpha), so tree-level "
        "e-e scattering (2 vertices) ~ alpha ~ 1/137."
    ),
    source="Wikipedia contributors, 'Feynman diagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Feynman_diagram",
    prerequisites=["conservation_laws"],
))

register_atom(Atom(
    atom_type="formula",
    name="cross_section",
    content=(
        "The scattering cross section sigma measures the probability of "
        "a scattering event. The differential cross section d sigma/d Omega "
        "gives the angular distribution. For Rutherford scattering: "
        "d sigma/d Omega = (Z1*Z2*e^2 / (4E))^2 / sin^4(theta/2). "
        "Total cross section is the integral over all solid angles. "
        "Units: barn (1 b = 10^-24 cm^2)."
    ),
    tier=7,
    domain="particle_physics",
    example=(
        "Rutherford scattering: Z1=2 (alpha), Z2=79 (gold), E=5 MeV, "
        "theta=90 deg. d sigma/d Omega = (2*79*1.44/(4*5))^2 / sin^4(45) "
        "= (56.88)^2 / 0.25 = 3235.33 / 0.25 = 12941 fm^2/sr."
    ),
    source="Wikipedia contributors, 'Cross section (physics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cross_section_(physics)",
    prerequisites=["conservation_laws"],
))

register_atom(Atom(
    atom_type="formula",
    name="decay_width",
    content=(
        "The decay width Gamma of an unstable particle is related to its "
        "mean lifetime tau by Gamma = hbar / tau. The partial width "
        "Gamma_i for decay channel i gives the branching ratio "
        "BR_i = Gamma_i / Gamma_total. The total width is the sum of all "
        "partial widths. A broader width means a shorter lifetime."
    ),
    tier=6,
    domain="particle_physics",
    example=(
        "W boson: Gamma_total = 2.085 GeV, tau = hbar/Gamma = "
        "6.582e-25 GeV*s / 2.085 GeV = 3.157e-25 s. "
        "BR(W -> e nu) = 0.1071, so Gamma_e = 0.1071 * 2.085 = 0.2233 GeV."
    ),
    source="Wikipedia contributors, 'Particle decay', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Particle_decay",
    prerequisites=["half_life"],
))

register_atom(Atom(
    atom_type="formula",
    name="invariant_mass",
    content=(
        "The invariant mass M of a system of particles is computed from "
        "the total four-momentum: M^2 c^4 = (sum E_i)^2 - (sum p_i c)^2. "
        "For a single particle, M^2 c^4 = E^2 - (pc)^2. The invariant "
        "mass is the same in all reference frames, making it useful for "
        "identifying resonances in collider experiments."
    ),
    tier=6,
    domain="particle_physics",
    example=(
        "Two photons with E1=50 GeV, E2=50 GeV, angle 180 deg: "
        "M^2 = (100)^2 - (50-(-50))^2 = 10000 - 10000 = 0 (massless). "
        "At 90 deg: M^2 = (100)^2 - (50^2+50^2) = 10000 - 5000, "
        "M = sqrt(5000) = 70.71 GeV."
    ),
    source="Wikipedia contributors, 'Invariant mass', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Invariant_mass",
    prerequisites=["relativistic_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="cms_energy",
    content=(
        "The centre-of-mass energy sqrt(s) in a collider experiment is "
        "the total energy available for particle creation. For two beams "
        "of equal energy E colliding head-on: sqrt(s) = 2E. For a fixed "
        "target experiment with beam energy E and target mass m: "
        "sqrt(s) = sqrt(2mE + 2m^2) ~ sqrt(2mE) for E >> m."
    ),
    tier=5,
    domain="particle_physics",
    example=(
        "LHC: two proton beams at E = 6500 GeV each. "
        "sqrt(s) = 2 * 6500 = 13000 GeV = 13 TeV. "
        "Fixed target equivalent: E = s/(2m) = 13000^2/(2*0.938) "
        "= 9.01e7 GeV = 90.1 PeV."
    ),
    source="Wikipedia contributors, 'Center-of-momentum frame', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Center-of-momentum_frame",
    prerequisites=["relativistic_energy"],
))

register_atom(Atom(
    atom_type="definition",
    name="symmetry_group",
    content=(
        "The Standard Model of particle physics is based on the gauge "
        "symmetry group SU(3)_C x SU(2)_L x U(1)_Y. SU(3)_C describes "
        "the strong interaction (quantum chromodynamics) with 8 gluons. "
        "SU(2)_L x U(1)_Y describes the electroweak interaction with "
        "W+, W-, Z, and photon. Spontaneous symmetry breaking via the "
        "Higgs mechanism gives mass to W and Z bosons."
    ),
    tier=7,
    domain="particle_physics",
    example=(
        "SU(2) has 2^2-1 = 3 generators (Pauli matrices). "
        "SU(3) has 3^2-1 = 8 generators (Gell-Mann matrices). "
        "U(1) has 1 generator. Total gauge bosons: 8 + 3 + 1 = 12."
    ),
    source="Wikipedia contributors, 'Standard Model', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Standard_Model",
    prerequisites=["group_axiom_check"],
))
