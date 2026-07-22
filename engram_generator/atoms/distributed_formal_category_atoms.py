"""Knowledge atoms for distributed systems, formal languages, and category theory.

Covers distributed consensus algorithms, automata theory and formal
grammars, and abstract categorical constructions. Each atom stores the
authoritative definition sourced from Wikipedia, a worked example, tier,
domain, source citation, URL, and prerequisite atoms.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Formal Languages (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="nfa_to_dfa",
    content=(
        "The powerset construction (subset construction) converts a "
        "nondeterministic finite automaton (NFA) into a deterministic "
        "finite automaton (DFA) that recognises the same language. Each "
        "state of the DFA corresponds to a set of NFA states. For an NFA "
        "with n states, the resulting DFA may have up to 2^n states."
    ),
    example=(
        "NFA: states={q0,q1,q2}, alphabet={a,b}, start=q0, accept={q2}, "
        "transitions: q0-a->{q0,q1}, q0-b->{q0}, q1-b->{q2}. "
        "DFA: start={q0}, {q0}-a->{q0,q1}, {q0}-b->{q0}, "
        "{q0,q1}-a->{q0,q1}, {q0,q1}-b->{q0,q2}*, {q0,q2}-a->{q0,q1}, "
        "{q0,q2}-b->{q0}. Accept states: any set containing q2."
    ),
    tier=5,
    domain="formal_languages",
    source="Wikipedia contributors, 'Powerset construction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Powerset_construction",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="regex_to_nfa",
    content=(
        "Thompson's construction converts a regular expression into an "
        "equivalent NFA. The algorithm is recursive: for each operator "
        "(concatenation, union, Kleene star), it builds a small NFA "
        "fragment and combines fragments. The resulting NFA has at most "
        "2s states for a regex of length s, with exactly one accept state."
    ),
    example=(
        "Regex: (a|b)*c. Thompson NFA: q0 --eps--> q1 (start of star), "
        "q1 --a--> q2, q1 --b--> q3, q2 --eps--> q4, q3 --eps--> q4, "
        "q4 --eps--> q1 (loop back), q4 --eps--> q5, q5 --c--> q6 (accept). "
        "Accepts: 'c', 'ac', 'bc', 'abc', 'aabbc', etc."
    ),
    tier=5,
    domain="formal_languages",
    source="Wikipedia contributors, 'Thompson's construction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thompson%27s_construction",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="cfg_derivation",
    content=(
        "A derivation in a context-free grammar (CFG) is a sequence of "
        "production rule applications that transforms the start symbol "
        "into a string of terminals. A leftmost derivation always expands "
        "the leftmost nonterminal first. A rightmost derivation expands "
        "the rightmost nonterminal first."
    ),
    example=(
        "Grammar: S -> aSb | ab. Derive 'aaabbb': "
        "S => aSb => aaSbb => aaabbb. Three steps, leftmost derivation."
    ),
    tier=5,
    domain="formal_languages",
    source="Wikipedia contributors, 'Context-free grammar', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Context-free_grammar",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="cfg_ambiguity",
    content=(
        "A context-free grammar is ambiguous if there exists at least one "
        "string that has two or more distinct leftmost derivations (or "
        "equivalently, two or more distinct parse trees). An inherently "
        "ambiguous language is one for which every CFG is ambiguous."
    ),
    example=(
        "Grammar: E -> E+E | E*E | id. String 'id+id*id' has two parse "
        "trees: (id+id)*id and id+(id*id). The grammar is ambiguous. "
        "Fix: introduce precedence via E -> E+T | T, T -> T*F | F, F -> id."
    ),
    tier=6,
    domain="formal_languages",
    source="Wikipedia contributors, 'Ambiguous grammar', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ambiguous_grammar",
    prerequisites=["cfg_derivation"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="pushdown_simulate",
    content=(
        "A pushdown automaton (PDA) extends a finite automaton with a "
        "stack, giving it the power to recognise context-free languages. "
        "At each step, based on the current state, input symbol, and top "
        "of stack, the PDA transitions to a new state and pushes or pops "
        "stack symbols. A string is accepted if the PDA reaches an accept "
        "state (or empties the stack, depending on acceptance mode)."
    ),
    example=(
        "PDA for a^n b^n: states={q0,q1,qf}, start=q0, accept={qf}. "
        "Rules: (q0,a,Z)->push A; (q0,a,A)->push A; (q0,b,A)->pop,goto q1; "
        "(q1,b,A)->pop; (q1,eps,Z)->qf. Input 'aabb': "
        "q0,aabb,Z -> q0,abb,AZ -> q0,bb,AAZ -> q1,b,AZ -> q1,eps,Z -> qf. ACCEPT."
    ),
    tier=5,
    domain="formal_languages",
    source="Wikipedia contributors, 'Pushdown automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pushdown_automaton",
    prerequisites=["cfg_derivation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="pumping_lemma",
    content=(
        "The pumping lemma for regular languages states: if L is a regular "
        "language, then there exists a pumping length p such that any "
        "string s in L with |s| >= p can be split as s = xyz where "
        "|y| > 0, |xy| <= p, and xy^i z is in L for all i >= 0. Used "
        "to prove a language is NOT regular by contradiction."
    ),
    example=(
        "Prove {a^n b^n | n>=0} is not regular. Assume pumping length p. "
        "Take s = a^p b^p, |s| = 2p >= p. Any split xyz with |xy| <= p "
        "means y = a^k for some k > 0. Pump: xy^2 z = a^{p+k} b^p. "
        "Since p+k != p, this is not in L. Contradiction."
    ),
    tier=6,
    domain="formal_languages",
    source="Wikipedia contributors, 'Pumping lemma for regular languages', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages",
    prerequisites=["nfa_to_dfa"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="chomsky_normal",
    content=(
        "Chomsky normal form (CNF) is a simplified form of context-free "
        "grammars where every production is either A -> BC (two "
        "nonterminals) or A -> a (single terminal). Any CFG can be "
        "converted to CNF. The CYK parsing algorithm requires CNF input."
    ),
    example=(
        "Grammar: S -> aSb | ab. Convert to CNF: introduce A->a, B->b. "
        "S -> ASB | AB, where S->ASB needs splitting: S -> AS1, S1 -> SB. "
        "Final CNF: S -> AS1 | AB, S1 -> SB, A -> a, B -> b."
    ),
    tier=6,
    domain="formal_languages",
    source="Wikipedia contributors, 'Chomsky normal form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chomsky_normal_form",
    prerequisites=["cfg_derivation"],
))

register_atom(Atom(
    atom_type="definition",
    name="language_classify",
    content=(
        "The Chomsky hierarchy classifies formal languages into four types: "
        "Type 3 (regular, recognised by finite automata), Type 2 "
        "(context-free, recognised by pushdown automata), Type 1 "
        "(context-sensitive, recognised by linear bounded automata), and "
        "Type 0 (recursively enumerable, recognised by Turing machines). "
        "Each type is a proper subset of the next."
    ),
    example=(
        "a*b* is Type 3 (regular, matched by DFA). "
        "a^n b^n is Type 2 (context-free, needs PDA). "
        "a^n b^n c^n is Type 1 (context-sensitive). "
        "{w | w encodes a halting TM} is Type 0 only."
    ),
    tier=6,
    domain="formal_languages",
    source="Wikipedia contributors, 'Chomsky hierarchy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chomsky_hierarchy",
    prerequisites=["pushdown_simulate", "pumping_lemma"],
))


# ---------------------------------------------------------------------------
# Distributed Systems (tier 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="lamport_clock",
    content=(
        "Lamport timestamps provide a partial ordering of events in a "
        "distributed system. Each process maintains a counter. On local "
        "event: increment counter. On send: increment and attach counter. "
        "On receive(msg, ts): counter = max(counter, ts) + 1. If event a "
        "causally precedes b, then L(a) < L(b), but not conversely."
    ),
    example=(
        "Process P1: event a (L=1), send to P2 (L=2). "
        "Process P2: local event (L=1), receive from P1 (L=max(1,2)+1=3), "
        "local event (L=4). Ordering: a(1) < send(2) < recv(3) < local(4)."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Lamport timestamp', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lamport_timestamp",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="vector_clock_compare",
    content=(
        "Vector clocks extend Lamport clocks to capture causality precisely. "
        "Each process maintains a vector of counters, one per process. "
        "V(a) < V(b) iff V(a)[i] <= V(b)[i] for all i and V(a) != V(b). "
        "If neither V(a) < V(b) nor V(b) < V(a), the events are concurrent."
    ),
    example=(
        "3 processes. P1=[2,0,0] sends to P2. P2 had [0,1,0], receives: "
        "P2 = [max(2,0), max(0,1)+1, max(0,0)] = [2,2,0]. "
        "Compare [2,0,0] vs [0,0,1]: neither dominates, so concurrent."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Vector clock', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Vector_clock",
    prerequisites=["lamport_clock"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="consensus_round",
    content=(
        "Distributed consensus requires a set of processes to agree on a "
        "single value despite failures. In synchronous rounds, each process "
        "broadcasts its value, collects responses, and applies a decision "
        "rule (e.g., majority). With f crash failures, f+1 rounds suffice. "
        "The FLP impossibility result shows consensus is impossible in "
        "asynchronous systems with even one crash failure."
    ),
    example=(
        "3 processes, f=1. Round 1: P1 proposes 'A', P2 proposes 'B', "
        "P3 proposes 'A'. All receive {A, B, A}. Majority rule: decide 'A'. "
        "If P2 crashes before sending, P1 and P3 see {A, -, A}, decide 'A'."
    ),
    tier=6,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Consensus (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Consensus_(computer_science)",
    prerequisites=["lamport_clock"],
))

register_atom(Atom(
    atom_type="theorem",
    name="cap_theorem",
    content=(
        "The CAP theorem (Brewer's theorem) states that a distributed data "
        "store cannot simultaneously provide more than two of three "
        "guarantees: Consistency (every read returns the most recent write), "
        "Availability (every request receives a non-error response), and "
        "Partition tolerance (the system operates despite network partitions). "
        "Since network partitions are unavoidable, the practical choice is "
        "between CP and AP systems."
    ),
    example=(
        "Network partition splits nodes {A,B} from {C}. CP system: A,B "
        "serve reads/writes, C refuses requests (unavailable but consistent). "
        "AP system: all nodes serve requests, but C may return stale data "
        "(available but eventually consistent). Example CP: HBase. Example AP: Cassandra."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'CAP theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/CAP_theorem",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="algorithm",
    name="consistent_hash_rebalance",
    content=(
        "Consistent hashing maps both data keys and nodes onto a circular "
        "hash space (ring). Each key is assigned to the first node "
        "encountered clockwise on the ring. When a node is added or "
        "removed, only K/n keys need to be remapped on average (K total "
        "keys, n nodes), compared to K keys in traditional hashing."
    ),
    example=(
        "Ring [0, 360). Nodes at positions: A=90, B=210, C=330. "
        "Key h(k1)=50 -> A (first node clockwise). Key h(k2)=150 -> B. "
        "Add node D=120: only keys in (90, 120] move from B to D. "
        "Keys in other ranges unchanged."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Consistent hashing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Consistent_hashing",
    prerequisites=["sorting"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="two_phase_commit",
    content=(
        "Two-phase commit (2PC) is a distributed transaction protocol. "
        "Phase 1 (Prepare): coordinator asks all participants to vote "
        "commit or abort. Phase 2 (Commit/Abort): if all vote commit, "
        "coordinator sends commit; if any votes abort, coordinator sends "
        "abort. 2PC is blocking: if the coordinator fails after Phase 1, "
        "participants may be stuck waiting."
    ),
    example=(
        "Coordinator C, participants P1, P2. C sends PREPARE. "
        "P1 votes COMMIT, P2 votes COMMIT. C sends COMMIT to both. "
        "If P2 had voted ABORT, C would send ABORT to both. "
        "Blocking scenario: C crashes after collecting votes but before "
        "sending decision -- P1 and P2 hold locks indefinitely."
    ),
    tier=6,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Two-phase commit protocol', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Two-phase_commit_protocol",
    prerequisites=["consensus_round"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="raft_election",
    content=(
        "Raft is a consensus algorithm where one node is elected leader. "
        "Each node is in one of three states: follower, candidate, or "
        "leader. Election starts when a follower's election timeout fires. "
        "It becomes a candidate, increments its term, votes for itself, "
        "and requests votes from others. A candidate wins if it receives "
        "votes from a majority. Only one leader per term."
    ),
    example=(
        "5 nodes, term=3. Node B's timeout fires, becomes candidate for "
        "term 4, votes for itself (1/5). Sends RequestVote to A,C,D,E. "
        "A,C vote yes (3/5 = majority). B becomes leader for term 4. "
        "D,E respond later but election already decided."
    ),
    tier=6,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Raft (algorithm)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Raft_(algorithm)",
    prerequisites=["consensus_round"],
))

register_atom(Atom(
    atom_type="definition",
    name="crdt_merge",
    content=(
        "A Conflict-free Replicated Data Type (CRDT) is a data structure "
        "that can be replicated across multiple nodes, updated independently "
        "and concurrently, and merged deterministically into a consistent "
        "state without coordination. The merge operation must be commutative, "
        "associative, and idempotent. Examples: G-Counter, PN-Counter, "
        "OR-Set, LWW-Register."
    ),
    example=(
        "G-Counter with 3 replicas. Initial: [0,0,0]. "
        "Replica 0 increments: [1,0,0]. Replica 2 increments twice: [0,0,2]. "
        "Merge: [max(1,0), max(0,0), max(0,2)] = [1,0,2]. "
        "Counter value = sum = 3."
    ),
    tier=5,
    domain="distributed_systems",
    source="Wikipedia contributors, 'Conflict-free replicated data type', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type",
    prerequisites=["vector_clock_compare"],
))


# ---------------------------------------------------------------------------
# Category Theory (tier 7-8)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="morphism_compose",
    content=(
        "In category theory, a morphism (arrow) is a structure-preserving "
        "map between objects. Composition of morphisms f: A -> B and "
        "g: B -> C yields g . f: A -> C. Composition must be associative: "
        "h . (g . f) = (h . g) . f. Every object A has an identity "
        "morphism id_A such that f . id_A = f and id_B . f = f."
    ),
    example=(
        "Category Set: objects are sets, morphisms are functions. "
        "f: {1,2} -> {a,b} with f(1)=a, f(2)=b. "
        "g: {a,b} -> {x} with g(a)=x, g(b)=x. "
        "g . f: {1,2} -> {x} with (g.f)(1)=x, (g.f)(2)=x."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Morphism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Morphism",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="functor_apply",
    content=(
        "A functor F: C -> D maps objects and morphisms between categories "
        "while preserving composition and identity. For objects: F(A) is "
        "an object in D. For morphisms f: A -> B: F(f): F(A) -> F(B). "
        "Preservation: F(g . f) = F(g) . F(f) and F(id_A) = id_{F(A)}."
    ),
    example=(
        "Forgetful functor U: Grp -> Set sends each group to its underlying "
        "set and each group homomorphism to the same function. "
        "U(Z_6) = {0,1,2,3,4,5}. U(phi: Z_6 -> Z_3) = phi as a set map. "
        "U(id_{Z_6}) = id_{U(Z_6)} = identity function on {0,1,2,3,4,5}."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Functor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Functor",
    prerequisites=["morphism_compose"],
))

register_atom(Atom(
    atom_type="definition",
    name="natural_transform",
    content=(
        "A natural transformation eta: F => G between functors F, G: C -> D "
        "assigns to each object A in C a morphism eta_A: F(A) -> G(A) in D "
        "such that for every morphism f: A -> B in C, the naturality square "
        "commutes: G(f) . eta_A = eta_B . F(f)."
    ),
    example=(
        "F = identity functor on Set, G = powerset functor. "
        "eta_A: A -> P(A) sends x to {x} (singleton). "
        "Naturality: for f: A -> B, P(f)({x}) = {f(x)} = eta_B(f(x)). "
        "Check: P(f)(eta_A(x)) = P(f)({x}) = {f(x)} = eta_B(f(x)). Commutes."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Natural transformation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Natural_transformation",
    prerequisites=["functor_apply"],
))

register_atom(Atom(
    atom_type="definition",
    name="product_category",
    content=(
        "The categorical product of objects A and B is an object A x B "
        "together with projection morphisms pi_1: A x B -> A and "
        "pi_2: A x B -> B, satisfying the universal property: for any "
        "object C with morphisms f: C -> A and g: C -> B, there exists a "
        "unique morphism <f,g>: C -> A x B such that pi_1 . <f,g> = f "
        "and pi_2 . <f,g> = g."
    ),
    example=(
        "In Set: product of {a,b} and {1,2} is {a,b} x {1,2} = "
        "{(a,1),(a,2),(b,1),(b,2)} with pi_1((a,1))=a, pi_2((a,1))=1. "
        "For f: {*} -> {a,b} with f(*)=a and g: {*} -> {1,2} with g(*)=2, "
        "<f,g>(*) = (a,2)."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Product (category theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Product_(category_theory)",
    prerequisites=["morphism_compose"],
))

register_atom(Atom(
    atom_type="definition",
    name="coproduct_category",
    content=(
        "The categorical coproduct of objects A and B is an object A + B "
        "with injection morphisms iota_1: A -> A + B and iota_2: B -> A + B, "
        "satisfying the universal property: for any object C with morphisms "
        "f: A -> C and g: B -> C, there exists a unique morphism "
        "[f,g]: A + B -> C such that [f,g] . iota_1 = f and [f,g] . iota_2 = g."
    ),
    example=(
        "In Set: coproduct of {a,b} and {1,2} is the disjoint union "
        "{a,b,1,2} (tagged). iota_1(a) = a_left, iota_2(1) = 1_right. "
        "For f: {a,b} -> {x} and g: {1,2} -> {x}, "
        "[f,g](a_left) = x, [f,g](1_right) = x."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Coproduct', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coproduct",
    prerequisites=["product_category"],
))

register_atom(Atom(
    atom_type="definition",
    name="adjunction_check",
    content=(
        "An adjunction between categories C and D consists of functors "
        "F: C -> D (left adjoint) and G: D -> C (right adjoint) with a "
        "natural bijection Hom_D(F(A), B) ~ Hom_C(A, G(B)) for all "
        "objects A in C and B in D. Equivalently, there exist natural "
        "transformations eta: Id_C => GF (unit) and epsilon: FG => Id_D "
        "(counit) satisfying the triangle identities."
    ),
    example=(
        "Free-forgetful adjunction: F: Set -> Grp sends a set S to the "
        "free group F(S). G: Grp -> Set is the forgetful functor. "
        "Hom_Grp(F({a,b}), Z) ~ Hom_Set({a,b}, U(Z)) = Z x Z. "
        "Each group homomorphism from the free group on {a,b} is determined "
        "by choosing images of a and b in Z."
    ),
    tier=8,
    domain="category_theory",
    source="Wikipedia contributors, 'Adjoint functors', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Adjoint_functors",
    prerequisites=["functor_apply", "natural_transform"],
))

register_atom(Atom(
    atom_type="theorem",
    name="yoneda_apply",
    content=(
        "The Yoneda lemma states that for a locally small category C, "
        "a functor F: C^op -> Set, and an object A in C, the set of "
        "natural transformations Nat(Hom(A,-), F) is in bijection with "
        "F(A). The bijection sends a natural transformation alpha to "
        "alpha_A(id_A). This is one of the most fundamental results in "
        "category theory."
    ),
    example=(
        "C = Set, A = {*} (singleton), F = Id (identity functor). "
        "Hom({*}, X) ~ X for any set X. Nat(Hom({*},-), Id) ~ Id({*}) = {*}. "
        "The unique natural transformation is the identity on each "
        "component: eta_X: Hom({*},X) -> X sends f to f(*)."
    ),
    tier=8,
    domain="category_theory",
    source="Wikipedia contributors, 'Yoneda lemma', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Yoneda_lemma",
    prerequisites=["natural_transform"],
))

register_atom(Atom(
    atom_type="definition",
    name="limit_compute",
    content=(
        "A limit of a diagram D: J -> C is an object L with morphisms "
        "(a cone) from L to each object in the diagram, satisfying the "
        "universal property: any other cone factors uniquely through L. "
        "Products are limits of discrete diagrams. Equalisers are limits "
        "of parallel-pair diagrams. Pullbacks are limits of cospan diagrams."
    ),
    example=(
        "Pullback of f: A -> C and g: B -> C in Set. "
        "A = {1,2,3}, B = {a,b}, C = {x,y}. f(1)=x, f(2)=x, f(3)=y. "
        "g(a)=x, g(b)=y. Pullback P = {(a,c) in AxB | f(a)=g(c)} = "
        "{(1,a),(2,a),(3,b)} with pi_1, pi_2 projections."
    ),
    tier=7,
    domain="category_theory",
    source="Wikipedia contributors, 'Limit (category theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limit_(category_theory)",
    prerequisites=["product_category"],
))
