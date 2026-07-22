"""Knowledge atoms for statistical mechanics and discrete mathematics.

Registers formula, theorem, and algorithm atoms covering partition
functions, quantum statistics, Ising model, graph polynomials,
Ramsey theory, matroid theory, and combinatorial enumeration.
Each atom includes a worked example with known input/output for
independent verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# =========================================================================
# Statistical Mechanics (tier 5-7)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="partition_function_stat",
    content=(
        "The canonical partition function Z sums over all microstates i: "
        "Z = sum_i exp(-E_i / (k_B T)), where E_i is the energy of "
        "microstate i, k_B is the Boltzmann constant, and T is the "
        "absolute temperature. All thermodynamic quantities can be "
        "derived from Z: free energy F = -k_B T ln(Z), average energy "
        "<E> = -d(ln Z)/d(beta) where beta = 1/(k_B T)."
    ),
    example=(
        "Two-level system with E_0=0, E_1=epsilon, at beta*epsilon=1: "
        "Z = exp(0) + exp(-1) = 1 + 0.3679 = 1.3679"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Partition function (statistical mechanics)', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Partition_function_(statistical_mechanics)",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="boltzmann_probability",
    content=(
        "The Boltzmann distribution gives the probability of a system "
        "being in microstate i: P_i = exp(-E_i / (k_B T)) / Z, where "
        "Z is the partition function. This is the fundamental probability "
        "distribution of statistical mechanics for systems in thermal "
        "equilibrium with a heat bath at temperature T."
    ),
    example=(
        "Two-level system E_0=0, E_1=epsilon, beta*epsilon=1: "
        "P_0 = 1/1.3679 = 0.7311, P_1 = 0.3679/1.3679 = 0.2689"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Boltzmann distribution', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Boltzmann_distribution",
    prerequisites=["partition_function_stat"],
))

register_atom(Atom(
    atom_type="formula",
    name="average_energy",
    content=(
        "The average energy of a canonical ensemble is: "
        "<E> = sum_i E_i * P_i = (1/Z) sum_i E_i exp(-beta E_i), "
        "equivalently <E> = -d(ln Z)/d(beta). For a simple harmonic "
        "oscillator, <E> = hbar*omega/(exp(beta*hbar*omega) - 1) + "
        "hbar*omega/2."
    ),
    example=(
        "Two-level system E_0=0, E_1=1 (units of k_B T): "
        "<E> = 0*0.7311 + 1*0.2689 = 0.2689 k_B T"
    ),
    tier=6,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Canonical ensemble', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Canonical_ensemble",
    prerequisites=["boltzmann_probability"],
))

register_atom(Atom(
    atom_type="formula",
    name="fermi_dirac",
    content=(
        "The Fermi-Dirac distribution gives the average occupation "
        "number of a single-particle state with energy epsilon for "
        "fermions: f(epsilon) = 1 / (exp((epsilon - mu)/(k_B T)) + 1), "
        "where mu is the chemical potential (Fermi energy at T=0). "
        "At T=0, f = 1 for epsilon < mu and f = 0 for epsilon > mu "
        "(sharp Fermi surface)."
    ),
    example=(
        "epsilon=0.5 eV, mu=0.3 eV, k_B T=0.1 eV: "
        "f = 1/(exp((0.5-0.3)/0.1) + 1) = 1/(exp(2) + 1) = "
        "1/(7.389 + 1) = 0.1192"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Fermi-Dirac statistics', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Fermi%E2%80%93Dirac_statistics",
    prerequisites=["boltzmann_probability"],
))

register_atom(Atom(
    atom_type="formula",
    name="bose_einstein",
    content=(
        "The Bose-Einstein distribution gives the average occupation "
        "number of a single-particle state with energy epsilon for "
        "bosons: n(epsilon) = 1 / (exp((epsilon - mu)/(k_B T)) - 1). "
        "Unlike fermions, multiple bosons can occupy the same state. "
        "For photons, mu = 0."
    ),
    example=(
        "Photon gas, epsilon=0.2 eV, mu=0, k_B T=0.1 eV: "
        "n = 1/(exp(0.2/0.1) - 1) = 1/(exp(2) - 1) = "
        "1/(7.389 - 1) = 0.1565"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Bose-Einstein statistics', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Bose%E2%80%93Einstein_statistics",
    prerequisites=["boltzmann_probability"],
))

register_atom(Atom(
    atom_type="formula",
    name="ising_model",
    content=(
        "The Ising model Hamiltonian for a system of N spins s_i = +/-1 "
        "is H = -J sum_{<i,j>} s_i s_j - h sum_i s_i, where J is the "
        "coupling constant (J > 0 ferromagnetic, J < 0 antiferromagnetic), "
        "h is the external magnetic field, and <i,j> denotes nearest "
        "neighbours. The partition function is Z = sum_{configs} exp(-beta H)."
    ),
    example=(
        "Two spins, J=1, h=0, beta=1: states (++), (+-), (-+), (--) "
        "with H = -1, +1, +1, -1. Z = 2*exp(1) + 2*exp(-1) = "
        "2*2.718 + 2*0.368 = 6.172"
    ),
    tier=6,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Ising model', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Ising_model",
    prerequisites=["partition_function_stat"],
))

register_atom(Atom(
    atom_type="formula",
    name="entropy_stat_mech",
    content=(
        "The Gibbs entropy of a statistical ensemble is "
        "S = -k_B sum_i P_i ln(P_i), where P_i is the probability of "
        "microstate i. For the canonical ensemble, this reduces to "
        "S = k_B (ln Z + beta <E>). For a microcanonical ensemble "
        "with Omega equally probable microstates, S = k_B ln(Omega) "
        "(Boltzmann entropy)."
    ),
    example=(
        "Microcanonical ensemble with Omega=6 microstates: "
        "S = k_B * ln(6) = 1.7918 k_B"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Entropy (statistical thermodynamics)', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Entropy_(statistical_thermodynamics)",
    prerequisites=["partition_function_stat"],
))

register_atom(Atom(
    atom_type="theorem",
    name="equipartition",
    content=(
        "The equipartition theorem states that each quadratic degree "
        "of freedom contributes (1/2) k_B T to the average energy of "
        "a system in thermal equilibrium. For a monatomic ideal gas "
        "(3 translational DOF), <E> = (3/2) k_B T per molecule. "
        "For a diatomic gas (3 translational + 2 rotational), "
        "<E> = (5/2) k_B T at moderate temperatures."
    ),
    example=(
        "Monatomic ideal gas at T=300K: <E> per molecule = "
        "(3/2) * 1.381e-23 * 300 = 6.214e-21 J"
    ),
    tier=5,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Equipartition theorem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Equipartition_theorem",
    prerequisites=["average_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="specific_heat",
    content=(
        "The specific heat at constant volume is C_V = dU/dT, where "
        "U is the internal energy. For an ideal gas, C_V = (f/2) N k_B "
        "where f is the number of degrees of freedom. The Einstein model "
        "of a solid gives C_V = 3Nk_B (x^2 e^x)/(e^x - 1)^2 where "
        "x = theta_E/T and theta_E is the Einstein temperature."
    ),
    example=(
        "Monatomic ideal gas (f=3), N=1 mole: "
        "C_V = (3/2) * 8.314 = 12.471 J/(mol K)"
    ),
    tier=6,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Specific heat capacity', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Specific_heat_capacity",
    prerequisites=["equipartition"],
))

register_atom(Atom(
    atom_type="formula",
    name="grand_canonical",
    content=(
        "The grand canonical partition function is "
        "Xi = sum_N sum_i exp(-beta(E_i - mu N)), where the sum is "
        "over all particle numbers N and all microstates i at each N. "
        "The grand potential is Phi = -k_B T ln(Xi) = U - TS - mu N. "
        "Average particle number: <N> = k_B T d(ln Xi)/d(mu)."
    ),
    example=(
        "Single orbital, mu=0, epsilon=1, beta=1: "
        "Xi = 1 + exp(-1) = 1.3679 (fermion). "
        "<N> = exp(-1)/1.3679 = 0.2689"
    ),
    tier=7,
    domain="statistical_mechanics",
    source=(
        "Wikipedia contributors, 'Grand canonical ensemble', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Grand_canonical_ensemble",
    prerequisites=["partition_function_stat", "fermi_dirac"],
))


# =========================================================================
# Discrete Mathematics -- extended (tier 5-6)
# =========================================================================

register_atom(Atom(
    atom_type="formula",
    name="generating_function",
    content=(
        "The ordinary generating function (OGF) of a sequence {a_n} is "
        "the formal power series A(x) = sum_{n=0}^{inf} a_n x^n. "
        "Common examples: 1/(1-x) generates {1,1,1,...}, "
        "1/(1-x)^2 generates {1,2,3,...}, e^x generates {1/n!}. "
        "The product of two OGFs corresponds to the convolution "
        "of their coefficient sequences."
    ),
    example=(
        "Fibonacci: F(x) = x/(1-x-x^2). Coefficient of x^6: "
        "F_6 = 8. Verification: 0,1,1,2,3,5,8"
    ),
    tier=6,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Generating function', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Generating_function",
    prerequisites=["polynomial_eval"],
))

register_atom(Atom(
    atom_type="theorem",
    name="ramsey_number",
    content=(
        "The Ramsey number R(s,t) is the smallest integer n such that "
        "every 2-colouring of the edges of K_n contains either a red "
        "K_s or a blue K_t. Known exact values include R(3,3)=6, "
        "R(3,4)=9, R(3,5)=14, R(4,4)=18. The existence of Ramsey "
        "numbers is guaranteed by Ramsey's theorem."
    ),
    example=(
        "R(3,3) = 6: in any 2-colouring of K_6, there must be a "
        "monochromatic triangle. K_5 can be 2-coloured with no "
        "monochromatic triangle (e.g. Petersen complement)."
    ),
    tier=5,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Ramsey's theorem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Ramsey%27s_theorem",
    prerequisites=["counting"],
))

register_atom(Atom(
    atom_type="theorem",
    name="burnside_counting",
    content=(
        "Burnside's lemma (Cauchy-Frobenius lemma) counts distinct "
        "objects under group symmetry: |X/G| = (1/|G|) sum_{g in G} |Fix(g)|, "
        "where Fix(g) is the set of elements fixed by group element g. "
        "This is fundamental to combinatorial enumeration modulo symmetry, "
        "such as counting distinct necklaces or colourings."
    ),
    example=(
        "Colour 4 beads in a necklace with 2 colours, rotation group Z_4: "
        "|Fix(e)|=16, |Fix(r)|=2, |Fix(r^2)|=4, |Fix(r^3)|=2. "
        "|X/G| = (16+2+4+2)/4 = 6 distinct necklaces."
    ),
    tier=6,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Burnside's lemma', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Burnside%27s_lemma",
    prerequisites=["counting", "group_axiom_check"],
))

register_atom(Atom(
    atom_type="theorem",
    name="hall_marriage",
    content=(
        "Hall's marriage theorem states that a bipartite graph G=(X,Y,E) "
        "has a perfect matching from X to Y if and only if for every "
        "subset S of X, |N(S)| >= |S|, where N(S) is the set of "
        "neighbours of S in Y. This necessary and sufficient condition "
        "is called Hall's condition."
    ),
    example=(
        "X={a,b,c}, Y={1,2,3}, edges: a-1, a-2, b-2, b-3, c-1, c-3. "
        "Check Hall's condition: |N({a})|=2>=1, |N({b})|=2>=1, "
        "|N({a,b})|=3>=2, |N({a,b,c})|=3>=3. "
        "Condition satisfied. Matching: a-2, b-3, c-1."
    ),
    tier=5,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Hall's marriage theorem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Hall%27s_marriage_theorem",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="definition",
    name="matroid_check",
    content=(
        "A matroid M = (E, I) consists of a finite ground set E and a "
        "collection I of independent sets satisfying: (1) the empty set "
        "is in I, (2) if A is in I and B is a subset of A, then B is in I "
        "(hereditary), (3) if A and B are in I and |A| < |B|, then there "
        "exists b in B\\A such that A union {b} is in I (augmentation)."
    ),
    example=(
        "Graphic matroid of K_3 (triangle): E={e1,e2,e3}, "
        "I = {{}, {e1}, {e2}, {e3}, {e1,e2}, {e1,e3}, {e2,e3}}. "
        "Rank = 2 (max independent set size). {e1,e2,e3} is dependent "
        "(cycle)."
    ),
    tier=6,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Matroid', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Matroid",
    prerequisites=["set_operations"],
))

register_atom(Atom(
    atom_type="formula",
    name="chromatic_polynomial",
    content=(
        "The chromatic polynomial P(G, k) counts the number of proper "
        "k-colourings of graph G. For a complete graph K_n: "
        "P(K_n, k) = k(k-1)(k-2)...(k-n+1) = k!/(k-n)!. "
        "For a tree on n vertices: P(T_n, k) = k(k-1)^{n-1}. "
        "Deletion-contraction: P(G, k) = P(G-e, k) - P(G/e, k)."
    ),
    example=(
        "Triangle K_3 with k=3 colours: "
        "P(K_3, 3) = 3 * 2 * 1 = 6 proper colourings."
    ),
    tier=6,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Chromatic polynomial', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Chromatic_polynomial",
    prerequisites=["polynomial_eval", "graph_reach"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="flow_network",
    content=(
        "The maximum flow problem finds the maximum rate of flow from "
        "source s to sink t in a network with edge capacities. The "
        "max-flow min-cut theorem (Ford-Fulkerson) states that the "
        "maximum flow equals the minimum cut capacity. The Edmonds-Karp "
        "algorithm uses BFS to find augmenting paths in O(VE^2)."
    ),
    example=(
        "Network: s->a (cap 10), s->b (cap 5), a->b (cap 15), "
        "a->t (cap 10), b->t (cap 10). Max flow = 15: "
        "s->a->t (10) + s->b->t (5)."
    ),
    tier=5,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Maximum flow problem', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Maximum_flow_problem",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="theorem",
    name="planar_check",
    content=(
        "A graph is planar if it can be drawn in the plane without "
        "edge crossings. By Kuratowski's theorem, a graph is planar "
        "iff it contains no subdivision of K_5 or K_{3,3}. Euler's "
        "formula for connected planar graphs: V - E + F = 2, which "
        "implies E <= 3V - 6 for simple graphs with V >= 3."
    ),
    example=(
        "K_4: V=4, E=6. Check: 6 <= 3*4-6 = 6. Equality holds, "
        "and K_4 is planar. K_5: V=5, E=10. Check: 10 > 3*5-6 = 9. "
        "Fails, so K_5 is not planar."
    ),
    tier=5,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Planar graph', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Planar_graph",
    prerequisites=["graph_reach"],
))

register_atom(Atom(
    atom_type="definition",
    name="lattice_operations",
    content=(
        "A lattice is a partially ordered set in which every two elements "
        "have a unique supremum (join, denoted a v b) and a unique infimum "
        "(meet, denoted a ^ b). A distributive lattice satisfies "
        "a ^ (b v c) = (a ^ b) v (a ^ c). A Boolean lattice is a "
        "complemented distributive lattice."
    ),
    example=(
        "Divisors of 12 under divisibility: {1,2,3,4,6,12}. "
        "meet(4,6) = gcd(4,6) = 2, join(4,6) = lcm(4,6) = 12."
    ),
    tier=5,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Lattice (order)', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Lattice_(order)",
    prerequisites=["set_operations", "gcd"],
))

register_atom(Atom(
    atom_type="formula",
    name="partition_function",
    content=(
        "The integer partition function p(n) counts the number of ways "
        "to write n as a sum of positive integers, disregarding order. "
        "The generating function is prod_{k=1}^{inf} 1/(1-x^k). "
        "Values: p(1)=1, p(2)=2, p(3)=3, p(4)=5, p(5)=7, p(10)=42, "
        "p(100)=190569292. Hardy-Ramanujan asymptotic: "
        "p(n) ~ exp(pi*sqrt(2n/3)) / (4n*sqrt(3))."
    ),
    example=(
        "p(5) = 7 partitions: 5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, "
        "1+1+1+1+1."
    ),
    tier=6,
    domain="discrete_mathematics",
    source=(
        "Wikipedia contributors, 'Partition function (number theory)', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Partition_function_(number_theory)",
    prerequisites=["counting", "generating_function"],
))
