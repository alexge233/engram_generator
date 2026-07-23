"""Atoms for bridge/deep topics: probability, DiffEq, abstract algebra, formal proofs.

These generators bridge the gap between new lower-tier domains and tiers 7-10.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Deeper Probability (tiers 3-5) ──────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="bayes_chain",
    content="Bayesian updating applies Bayes' theorem repeatedly as new evidence arrives: "
    "P(H|E1,E2) ∝ P(E2|H) * P(H|E1). Start with prior P(H), update with each observation. "
    "The posterior after one update becomes the prior for the next.",
    example="Prior P(H)=0.5. Evidence E1: P(E1|H)=0.8, P(E1|~H)=0.3. Posterior = 0.8*0.5/(0.8*0.5+0.3*0.5) = 0.4/0.55 = 0.727",
    tier=4, domain="probability",
    source="Wikipedia contributors, 'Bayesian inference', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bayesian_inference",
    prerequisites=["bayes_theorem", "conditional_prob"]))

register_atom(Atom(atom_type="definition", name="conditional_independence",
    content="Events A and B are conditionally independent given C if P(A∩B|C) = P(A|C)*P(B|C). "
    "This does NOT imply marginal independence. Example: two symptoms may be correlated in the "
    "population but conditionally independent given the disease.",
    example="P(A|C)=0.3, P(B|C)=0.4. If A,B independent given C: P(A,B|C) = 0.3*0.4 = 0.12. Check: P(A|B,C) should equal P(A|C) = 0.3",
    tier=4, domain="probability",
    source="Wikipedia contributors, 'Conditional independence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conditional_independence",
    prerequisites=["conditional_prob", "independence_test"]))

register_atom(Atom(atom_type="formula", name="joint_distribution",
    content="A joint probability distribution P(X,Y) gives the probability of each combination "
    "of values. The marginal P(X=x) = sum_y P(X=x, Y=y). Independence: P(X,Y) = P(X)*P(Y). "
    "Expected value: E[g(X,Y)] = sum_{x,y} g(x,y)*P(X=x,Y=y).",
    tier=5, domain="probability",
    source="Wikipedia contributors, 'Joint probability distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Joint_probability_distribution",
    prerequisites=["conditional_independence", "expected_value"]))

# ── Differential Equations (tiers 4-5) ──────────────────────────────

register_atom(Atom(atom_type="algorithm", name="separation_of_variables",
    content="For dy/dx = f(x)*g(y): rearrange to dy/g(y) = f(x)*dx, integrate both sides. "
    "Example: dy/dx = xy → dy/y = x dx → ln|y| = x^2/2 + C → y = Ae^{x^2/2}.",
    tier=4, domain="calculus",
    source="Wikipedia contributors, 'Separation of variables', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Separation_of_variables",
    prerequisites=["integral", "derivative"]))

register_atom(Atom(atom_type="algorithm", name="integrating_factor",
    content="For dy/dx + P(x)*y = Q(x): multiply by integrating factor mu(x) = e^{∫P(x)dx}. "
    "Then d/dx[mu*y] = mu*Q. Integrate both sides: y = (1/mu) * ∫mu*Q dx + C/mu.",
    tier=5, domain="calculus",
    source="Wikipedia contributors, 'Integrating factor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Integrating_factor",
    prerequisites=["separation_of_variables", "chain_rule"]))

register_atom(Atom(atom_type="algorithm", name="characteristic_equation",
    content="For a linear ODE with constant coefficients ay'' + by' + cy = 0: "
    "substitute y = e^{rx} to get ar^2 + br + c = 0. Distinct real roots r1,r2: y = C1*e^{r1*x} + C2*e^{r2*x}. "
    "Repeated root r: y = (C1 + C2*x)*e^{rx}. Complex roots a±bi: y = e^{ax}(C1*cos(bx) + C2*sin(bx)).",
    tier=5, domain="calculus",
    source="Wikipedia contributors, 'Characteristic equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Characteristic_equation_(calculus)",
    prerequisites=["quadratic", "separation_of_variables"]))

# ── Abstract Algebra (tiers 4-6) ────────────────────────────────────

register_atom(Atom(atom_type="definition", name="group_table",
    content="A group operation table (Cayley table) lists the product of every pair of elements. "
    "For Z_n under addition mod n: entry (i,j) = (i+j) mod n. Properties: closure, "
    "associativity, identity element, every element has an inverse. Z_4: {0,1,2,3} under + mod 4.",
    tier=4, domain="algebra",
    source="Wikipedia contributors, 'Cayley table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cayley_table",
    prerequisites=["modular"]))

register_atom(Atom(atom_type="definition", name="ring_arithmetic",
    content="A ring has two operations: addition (abelian group) and multiplication (associative, "
    "distributive over addition). Z_n is a ring under addition and multiplication mod n. "
    "Example: Z_6: 4*5 = 20 mod 6 = 2. A field is a ring where every nonzero element has a "
    "multiplicative inverse (Z_p for prime p).",
    tier=5, domain="algebra",
    source="Wikipedia contributors, 'Ring (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ring_(mathematics)",
    prerequisites=["group_table", "mod_inv"]))

register_atom(Atom(atom_type="definition", name="group_homomorphism",
    content="A homomorphism f: G -> H between groups preserves the operation: f(a*b) = f(a)*f(b). "
    "The kernel ker(f) = {g ∈ G : f(g) = e_H} is a normal subgroup. The image im(f) is a "
    "subgroup of H. First isomorphism theorem: G/ker(f) ≅ im(f).",
    tier=6, domain="algebra",
    source="Wikipedia contributors, 'Group homomorphism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Group_homomorphism",
    prerequisites=["group_table", "group_order"]))

# ── Formal Proofs (tiers 3-6) ──────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="direct_proof",
    content="A direct proof shows P → Q by assuming P is true and deriving Q through valid "
    "logical steps. Example: prove 'if n is even, then n^2 is even': assume n = 2k, "
    "then n^2 = 4k^2 = 2(2k^2), which is even. Each step must follow from axioms, definitions, "
    "or previously proved statements.",
    tier=3, domain="logic",
    source="Wikipedia contributors, 'Direct proof', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Direct_proof",
    prerequisites=["deduction_chain", "implication"]))

register_atom(Atom(atom_type="algorithm", name="proof_by_contradiction",
    content="Assume the negation of what you want to prove and derive a contradiction. "
    "Example: prove sqrt(2) is irrational — assume sqrt(2) = a/b in lowest terms, then "
    "2b^2 = a^2, so a is even, write a = 2k, then 2b^2 = 4k^2, so b is even, contradicting "
    "'lowest terms'. Therefore the assumption is false.",
    tier=4, domain="logic",
    source="Wikipedia contributors, 'Proof by contradiction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Proof_by_contradiction",
    prerequisites=["direct_proof", "negation"]))

register_atom(Atom(atom_type="algorithm", name="proof_by_cases",
    content="Proof by cases (exhaustion) divides the statement into cases that together cover "
    "all possibilities, then proves each case separately. Example: prove |xy| = |x||y|: "
    "Case 1: x >= 0, y >= 0. Case 2: x >= 0, y < 0. Case 3: x < 0, y >= 0. Case 4: x < 0, y < 0.",
    tier=4, domain="logic",
    source="Wikipedia contributors, 'Proof by exhaustion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Proof_by_exhaustion",
    prerequisites=["direct_proof"]))

register_atom(Atom(atom_type="algorithm", name="strong_induction",
    content="Strong induction assumes the statement holds for ALL values < n (not just n-1) "
    "when proving it for n. Base case: prove for n = 0 (or 1). Inductive step: assume P(k) "
    "for all k < n, prove P(n). Useful when the inductive step needs more than just the "
    "previous case. Example: every integer >= 2 has a prime factorisation.",
    tier=5, domain="logic",
    source="Wikipedia contributors, 'Mathematical induction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mathematical_induction#Strong_induction",
    prerequisites=["proof_by_induction"]))

register_atom(Atom(atom_type="algorithm", name="epsilon_delta_proof",
    content="An epsilon-delta proof shows a limit exists: for every epsilon > 0, there exists "
    "delta > 0 such that if 0 < |x - a| < delta, then |f(x) - L| < epsilon. "
    "Strategy: start from |f(x) - L|, express in terms of |x - a|, find delta that works.",
    tier=6, domain="analysis",
    source="Wikipedia contributors, 'Epsilon-delta definition of limit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/(%CE%B5,_%CE%B4)-definition_of_limit",
    prerequisites=["limit", "proof_by_contradiction"]))
