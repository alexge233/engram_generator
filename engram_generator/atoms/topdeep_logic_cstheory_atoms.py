"""Knowledge atoms for topology (deep), logic (ext), and CS theory (ext).

Covers path-connectedness, product/quotient topology, homotopy groups,
CNF/DNF conversion, proof by induction, complexity classes, and
streaming/randomised algorithms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Topology deep (tier 6-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="path_connected",
    content=(
        "A topological space X is path-connected if for every pair of "
        "points x, y in X, there exists a continuous function "
        "f: [0,1] -> X with f(0) = x and f(1) = y. Path-connectedness "
        "implies connectedness, but the converse is false in general. "
        "Every convex subset of R^n is path-connected."
    ),
    example=(
        "R^2 \\ {0}: path-connected because any two points can be joined "
        "by an arc avoiding the origin. The topologist's sine curve "
        "{(x, sin(1/x)) : x > 0} union {(0,0)} is connected but not "
        "path-connected."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Connected space', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Connected_space#Path_connectedness",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="product_topology",
    content=(
        "The product topology on a Cartesian product of topological spaces "
        "is the coarsest topology such that all projection maps are "
        "continuous. A basis for the product topology on X x Y consists "
        "of sets U x V where U is open in X and V is open in Y. For "
        "infinite products, only finitely many factors may differ from "
        "the full space in each basis element (box topology uses all "
        "open sets and is strictly finer)."
    ),
    example=(
        "Product topology on R x R: basis elements are open rectangles "
        "(a,b) x (c,d). The set (0,1) x (0,1) is open. The diagonal "
        "{(x,x): x in R} is closed in the product topology."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Product topology', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Product_topology",
    prerequisites=["open_closed_sets"],
))

register_atom(Atom(
    atom_type="definition",
    name="quotient_space_compute",
    content=(
        "A quotient space X/~ is formed by partitioning a topological "
        "space X by an equivalence relation ~ and giving the set of "
        "equivalence classes the quotient topology: a set U in X/~ is "
        "open iff its preimage under the canonical projection is open "
        "in X. Quotient spaces model gluing and identification."
    ),
    example=(
        "[0,1]/~ where 0 ~ 1: identifies endpoints, giving S^1 (circle). "
        "R/Z (reals mod integers) is also homeomorphic to S^1."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Quotient space (topology)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quotient_space_(topology)",
    prerequisites=["open_closed_sets", "continuity_topological"],
))

register_atom(Atom(
    atom_type="theorem",
    name="homotopy_group_compute",
    content=(
        "The n-th homotopy group pi_n(X, x0) is the set of homotopy "
        "classes of maps from the n-sphere S^n to X that send a basepoint "
        "to x0, with group operation given by concatenation. pi_1 is the "
        "fundamental group. For n >= 2, pi_n is abelian. Key results: "
        "pi_n(S^n) = Z, pi_k(S^n) = 0 for k < n."
    ),
    example=(
        "pi_1(S^1) = Z (fundamental group of circle is the integers). "
        "pi_1(S^2) = 0 (sphere is simply connected). "
        "pi_2(S^2) = Z, pi_3(S^2) = Z (Hopf fibration)."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Homotopy group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Homotopy_group",
    prerequisites=["path_connected", "continuity_topological"],
))

register_atom(Atom(
    atom_type="theorem",
    name="deformation_retract",
    content=(
        "A subspace A of X is a deformation retract if there exists a "
        "continuous map H: X x [0,1] -> X with H(x,0) = x, H(x,1) in A "
        "for all x, and H(a,t) = a for all a in A and t in [0,1]. A "
        "deformation retract is a homotopy equivalence, so X and A have "
        "the same homotopy type and thus the same homotopy groups."
    ),
    example=(
        "R^n \\ {0} deformation retracts onto S^{n-1} via "
        "H(x,t) = (1-t)x + t(x/|x|). The punctured plane R^2 \\ {0} "
        "deformation retracts onto S^1."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Deformation retract', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deformation_retract",
    prerequisites=["path_connected", "homotopy_group_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="surface_classification",
    content=(
        "The classification theorem for compact surfaces states that "
        "every closed connected surface is homeomorphic to either the "
        "sphere S^2, a connected sum of g tori (orientable, genus g), "
        "or a connected sum of k real projective planes (non-orientable). "
        "The Euler characteristic chi = 2 - 2g for orientable surfaces "
        "and chi = 2 - k for non-orientable surfaces."
    ),
    example=(
        "Torus T^2: genus g=1, chi = 2-2(1) = 0. "
        "Klein bottle: k=2 (non-orientable), chi = 2-2 = 0. "
        "Sphere S^2: g=0, chi = 2."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Classification theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Surface_(topology)#Classification_of_closed_surfaces",
    prerequisites=["homotopy_group_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="degree_of_map",
    content=(
        "The degree of a continuous map f: S^n -> S^n is an integer that "
        "measures how many times f wraps the domain around the codomain. "
        "Formally, it is the integer d such that f_*: H_n(S^n) -> H_n(S^n) "
        "is multiplication by d. The identity has degree 1, the antipodal "
        "map has degree (-1)^{n+1}, and a constant map has degree 0."
    ),
    example=(
        "f: S^1 -> S^1, f(z) = z^3 (complex multiplication): degree 3. "
        "Antipodal map on S^2: degree (-1)^3 = -1. "
        "f(z) = z^{-1} (inversion on S^1): degree -1."
    ),
    tier=7,
    domain="topology",
    source="Wikipedia contributors, 'Degree of a continuous mapping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Degree_of_a_continuous_mapping",
    prerequisites=["homotopy_group_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="nerve_theorem",
    content=(
        "The nerve theorem states that if U = {U_i} is a finite open "
        "cover of a paracompact space X such that every non-empty "
        "intersection of cover elements is contractible, then X is "
        "homotopy equivalent to the nerve N(U). The nerve is the "
        "abstract simplicial complex whose k-simplices correspond to "
        "(k+1)-fold intersections of cover elements."
    ),
    example=(
        "Cover S^1 with three overlapping arcs U1, U2, U3 where each "
        "pair intersects in a contractible arc and all three don't "
        "intersect: nerve is a triangle (boundary of 2-simplex), "
        "which is homotopy equivalent to S^1."
    ),
    tier=6,
    domain="topology",
    source="Wikipedia contributors, 'Nerve of a covering', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nerve_of_a_covering",
    prerequisites=["path_connected"],
))


# ---------------------------------------------------------------------------
# Logic ext (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="cnf_conversion",
    content=(
        "Conjunctive Normal Form (CNF) is a conjunction of clauses, where "
        "each clause is a disjunction of literals. Any propositional "
        "formula can be converted to CNF by: (1) eliminate biconditionals "
        "and implications, (2) push negations inward (De Morgan's laws), "
        "(3) distribute OR over AND."
    ),
    example=(
        "(p -> q) AND r: eliminate implication -> (NOT p OR q) AND r. "
        "Already in CNF: two clauses (NOT p OR q) and (r)."
    ),
    tier=5,
    domain="logic",
    source="Wikipedia contributors, 'Conjunctive normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjunctive_normal_form",
    prerequisites=["boolean_eval", "negation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dnf_conversion",
    content=(
        "Disjunctive Normal Form (DNF) is a disjunction of conjunctive "
        "clauses. Conversion: (1) eliminate implications and biconditionals, "
        "(2) push negations inward, (3) distribute AND over OR. "
        "Alternatively, DNF can be read directly from a truth table by "
        "forming a minterm for each row where the formula is true."
    ),
    example=(
        "NOT (p AND q): apply De Morgan -> NOT p OR NOT q. "
        "Already in DNF: two clauses (NOT p) and (NOT q)."
    ),
    tier=5,
    domain="logic",
    source="Wikipedia contributors, 'Disjunctive normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Disjunctive_normal_form",
    prerequisites=["boolean_eval", "negation"],
))

register_atom(Atom(
    atom_type="definition",
    name="logical_consequence",
    content=(
        "A formula phi is a logical consequence of a set of premises "
        "Gamma (written Gamma |= phi) if every interpretation that "
        "makes all formulas in Gamma true also makes phi true. "
        "Equivalently, Gamma |= phi iff the conjunction of Gamma with "
        "NOT phi is unsatisfiable."
    ),
    example=(
        "Premises: {p, p -> q}. Conclusion: q. "
        "Check: in any model where p is true and p -> q is true, "
        "q must be true (modus ponens). So {p, p -> q} |= q."
    ),
    tier=5,
    domain="logic",
    source="Wikipedia contributors, 'Logical consequence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logical_consequence",
    prerequisites=["implication", "truth_table"],
))

register_atom(Atom(
    atom_type="theorem",
    name="proof_by_induction_ext",
    content=(
        "Mathematical induction proves that a property P(n) holds for "
        "all natural numbers n >= n0 by: (1) Base case: prove P(n0), "
        "(2) Inductive step: assume P(k) (inductive hypothesis) and "
        "prove P(k+1). Strong induction assumes P(j) for all n0 <= j <= k."
    ),
    example=(
        "Prove sum(i, i=1..n) = n(n+1)/2. Base: n=1, 1 = 1*2/2 = 1. "
        "Inductive step: assume sum = k(k+1)/2, then "
        "sum(i=1..k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2."
    ),
    tier=6,
    domain="logic",
    source="Wikipedia contributors, 'Mathematical induction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mathematical_induction",
    prerequisites=["deduction_chain"],
))

register_atom(Atom(
    atom_type="definition",
    name="predicate_logic_validity",
    content=(
        "A formula in first-order predicate logic is valid if it is true "
        "in every interpretation (every domain, every assignment of "
        "predicates and functions). A formula is satisfiable if true in "
        "at least one interpretation. Validity of a closed formula can "
        "be checked by attempting to find a countermodel."
    ),
    example=(
        "forall x. (P(x) -> P(x)) is valid (tautology). "
        "forall x. P(x) OR forall x. NOT P(x) is NOT valid: "
        "countermodel with domain {a,b}, P(a)=T, P(b)=F."
    ),
    tier=6,
    domain="logic",
    source="Wikipedia contributors, 'Validity (logic)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Validity_(logic)",
    prerequisites=["logical_consequence", "quantifier_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="reductio_ad_absurdum",
    content=(
        "Proof by contradiction (reductio ad absurdum): to prove P, "
        "assume NOT P and derive a contradiction. Since the assumption "
        "leads to a contradiction, NOT P is false, so P must be true. "
        "This relies on the law of excluded middle (P or NOT P)."
    ),
    example=(
        "Prove sqrt(2) is irrational. Assume sqrt(2) = p/q in lowest "
        "terms. Then 2 = p^2/q^2, so p^2 = 2q^2, meaning p is even. "
        "Let p = 2k, then 4k^2 = 2q^2, so q^2 = 2k^2, meaning q is "
        "even. Contradiction: p/q was not in lowest terms."
    ),
    tier=5,
    domain="logic",
    source="Wikipedia contributors, 'Proof by contradiction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Proof_by_contradiction",
    prerequisites=["deduction_chain"],
))

register_atom(Atom(
    atom_type="theorem",
    name="soundness_completeness",
    content=(
        "Soundness: if Gamma |- phi (phi is provable from Gamma) then "
        "Gamma |= phi (phi is a logical consequence). Completeness "
        "(Goedel 1930): if Gamma |= phi then Gamma |- phi. Together they "
        "mean syntactic provability and semantic truth coincide for "
        "first-order logic. Goedel's incompleteness theorems show this "
        "fails for sufficiently strong arithmetic theories."
    ),
    example=(
        "In propositional logic: {p, p -> q} |- q (modus ponens is a "
        "sound rule). Completeness: any tautology has a proof in the "
        "standard proof system."
    ),
    tier=7,
    domain="logic",
    source="Wikipedia contributors, 'Goedel's completeness theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/G%C3%B6del%27s_completeness_theorem",
    prerequisites=["logical_consequence", "predicate_logic_validity"],
))

register_atom(Atom(
    atom_type="definition",
    name="tarski_truth",
    content=(
        "Tarski's undefinability theorem: the set of true sentences of "
        "a sufficiently expressive formal language cannot be defined "
        "within that language. Tarski's semantic definition of truth: "
        "a sentence 'snow is white' is true iff snow is white "
        "(T-schema). This provides a rigorous foundation for the "
        "correspondence theory of truth."
    ),
    example=(
        "T-schema: 'phi' is true in model M iff M |= phi. "
        "For atomic P(a): M |= P(a) iff the interpretation of a is "
        "in the interpretation of P."
    ),
    tier=6,
    domain="logic",
    source="Wikipedia contributors, 'Tarski\\'s undefinability theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Tarski%27s_undefinability_theorem",
    prerequisites=["predicate_logic_validity"],
))


# ---------------------------------------------------------------------------
# CS theory ext (tier 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="time_complexity_compute",
    content=(
        "The time complexity of an algorithm is the number of elementary "
        "operations as a function of input size n, expressed in big-O "
        "notation. Common classes: O(1) constant, O(log n) logarithmic, "
        "O(n) linear, O(n log n) linearithmic, O(n^2) quadratic, "
        "O(2^n) exponential."
    ),
    example=(
        "Binary search on sorted array of n elements: each step halves "
        "the search space. T(n) = T(n/2) + O(1), solution T(n) = O(log n)."
    ),
    tier=5,
    domain="computer_science",
    source="Wikipedia contributors, 'Time complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Time_complexity",
    prerequisites=["big_o"],
))

register_atom(Atom(
    atom_type="definition",
    name="space_complexity",
    content=(
        "The space complexity of an algorithm is the amount of memory "
        "required as a function of input size n. It includes both "
        "auxiliary space (extra space beyond input) and input space. "
        "PSPACE is the class of problems solvable in polynomial space."
    ),
    example=(
        "Merge sort: time O(n log n), space O(n) for auxiliary array. "
        "In-place quicksort: time O(n log n) average, space O(log n) "
        "for recursion stack."
    ),
    tier=5,
    domain="computer_science",
    source="Wikipedia contributors, 'Space complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Space_complexity",
    prerequisites=["big_o"],
))

register_atom(Atom(
    atom_type="theorem",
    name="np_completeness_proof",
    content=(
        "A problem L is NP-complete if: (1) L is in NP (solutions can "
        "be verified in polynomial time), and (2) every problem in NP "
        "is polynomial-time reducible to L. To prove NP-completeness, "
        "show L is in NP and reduce a known NP-complete problem to L. "
        "Cook-Levin theorem: SAT is NP-complete."
    ),
    example=(
        "3-SAT is NP-complete: (1) given an assignment, verify all "
        "clauses in O(n). (2) Reduce SAT to 3-SAT by splitting long "
        "clauses with auxiliary variables. Since SAT is NP-complete "
        "(Cook-Levin), 3-SAT is too."
    ),
    tier=7,
    domain="computer_science",
    source="Wikipedia contributors, 'NP-completeness', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/NP-completeness",
    prerequisites=["time_complexity_compute"],
))

register_atom(Atom(
    atom_type="definition",
    name="complexity_class",
    content=(
        "Complexity classes group problems by resource requirements. "
        "P: decidable in polynomial time. NP: verifiable in polynomial "
        "time. co-NP: complement in NP. PSPACE: polynomial space. "
        "EXPTIME: exponential time. Inclusions: P <= NP <= PSPACE <= "
        "EXPTIME. Whether P = NP is the central open question."
    ),
    example=(
        "Sorting is in P: O(n log n). SAT is NP-complete. "
        "TQBF (true quantified boolean formula) is PSPACE-complete. "
        "Chess (generalised) is EXPTIME-complete."
    ),
    tier=6,
    domain="computer_science",
    source="Wikipedia contributors, 'Complexity class', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Complexity_class",
    prerequisites=["time_complexity_compute", "space_complexity"],
))

register_atom(Atom(
    atom_type="definition",
    name="circuit_complexity",
    content=(
        "Circuit complexity measures the size (number of gates) or "
        "depth of Boolean circuits needed to compute a function. "
        "Key classes: AC^0 (constant depth, polynomial size, unbounded "
        "fan-in), NC (polylog depth, polynomial size), P/poly "
        "(polynomial-size circuits, possibly non-uniform)."
    ),
    example=(
        "Parity of n bits requires depth Omega(log n) in bounded "
        "fan-in circuits (NC^1). Parity is NOT in AC^0 (cannot be "
        "computed by constant-depth circuits with AND/OR gates)."
    ),
    tier=6,
    domain="computer_science",
    source="Wikipedia contributors, 'Circuit complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Circuit_complexity",
    prerequisites=["complexity_class"],
))

register_atom(Atom(
    atom_type="definition",
    name="communication_complexity",
    content=(
        "Communication complexity measures the minimum number of bits "
        "two parties must exchange to compute a function f(x,y) where "
        "Alice holds x and Bob holds y. The deterministic communication "
        "complexity D(f) is the worst-case number of bits for the best "
        "protocol. Key lower bound technique: fooling sets."
    ),
    example=(
        "Equality EQ(x,y) = [x == y]: D(EQ) = n+1 bits deterministic "
        "(must send all bits). Randomised: O(log n) bits using fingerprinting "
        "(hash x, send hash, Bob compares)."
    ),
    tier=6,
    domain="computer_science",
    source="Wikipedia contributors, 'Communication complexity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Communication_complexity",
    prerequisites=["complexity_class"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="streaming_algorithm",
    content=(
        "A streaming algorithm processes input as a single pass over a "
        "data stream using sublinear (typically O(log n) or O(sqrt(n))) "
        "space. Key algorithms: Count-Min Sketch for frequency estimation, "
        "HyperLogLog for cardinality estimation, Misra-Gries for heavy "
        "hitters, reservoir sampling for uniform samples."
    ),
    example=(
        "Distinct element counting with Flajolet-Martin: hash each "
        "element, track max trailing zeros. If max trailing zeros = r, "
        "estimate distinct count as 2^r. For stream [a,b,a,c,b,a]: "
        "3 distinct elements, estimate 2^(~1.6) approx 3."
    ),
    tier=5,
    domain="computer_science",
    source="Wikipedia contributors, 'Streaming algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Streaming_algorithm",
    prerequisites=["space_complexity"],
))

register_atom(Atom(
    atom_type="definition",
    name="randomised_complexity",
    content=(
        "Randomised complexity classes use probabilistic Turing machines. "
        "BPP: bounded-error probabilistic polynomial time (error < 1/3 "
        "on both sides). RP: one-sided error (no false positives). "
        "ZPP: zero-error, expected polynomial time (ZPP = RP intersect "
        "co-RP). It is known that BPP is in PSPACE; whether P = BPP "
        "is a major open question (widely believed true)."
    ),
    example=(
        "Primality testing (Miller-Rabin): in RP (if composite, detects "
        "with probability >= 3/4 per round; if prime, always says prime). "
        "AKS makes it polynomial deterministic, so PRIMES is in P."
    ),
    tier=6,
    domain="computer_science",
    source="Wikipedia contributors, 'BPP (complexity)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/BPP_(complexity)",
    prerequisites=["complexity_class"],
))
