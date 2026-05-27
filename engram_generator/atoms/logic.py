"""Knowledge atoms for logic and formal reasoning."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── Tier 0 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="boolean_eval",
    content=(
        "Boolean algebra operates on two values: True (1) and False (0). "
        "The three fundamental operations are AND (conjunction), OR "
        "(disjunction), and NOT (negation). AND returns True only when "
        "both operands are True. OR returns True when at least one operand "
        "is True. NOT inverts a single value. Evaluation follows operator "
        "precedence: NOT first, then AND, then OR."
    ),
    tier=0, domain="logic",
    source="Wikipedia contributors, 'Boolean algebra', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Boolean_algebra",
))

register_atom(Atom(
    atom_type="definition",
    name="truth_table",
    content=(
        "A truth table lists all possible combinations of truth values for "
        "the input variables of a logical formula and shows the resulting "
        "output for each combination. For n variables, there are 2^n rows. "
        "Truth tables provide a mechanical method to determine validity, "
        "satisfiability, and equivalence of logical formulas."
    ),
    tier=0, domain="logic",
    source="Wikipedia contributors, 'Truth table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Truth_table",
))

register_atom(Atom(
    atom_type="definition",
    name="negation",
    content=(
        "Negation (NOT) flips a truth value: NOT True = False, NOT False = True. "
        "De Morgan's laws govern negation of compound expressions: "
        "NOT (A AND B) = (NOT A) OR (NOT B); "
        "NOT (A OR B) = (NOT A) AND (NOT B). "
        "Double negation: NOT (NOT A) = A."
    ),
    tier=0, domain="logic",
    source="Wikipedia contributors, 'Negation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Negation",
))

# ── Tier 1 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="implication",
    content=(
        "Material implication (p -> q) is False only when p is True and q "
        "is False. In all other cases it is True. Equivalently, "
        "p -> q = (NOT p) OR q. The statement 'if it rains, the ground "
        "is wet' is only falsified when it rains but the ground is dry."
    ),
    tier=1, domain="logic",
    source="Wikipedia contributors, 'Material conditional', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Material_conditional",
    prerequisites=["boolean_eval"],
))

register_atom(Atom(
    atom_type="definition",
    name="biconditional",
    content=(
        "The biconditional (p <-> q) is True when both p and q have the "
        "same truth value. Equivalently, p <-> q = (p -> q) AND (q -> p). "
        "It reads 'p if and only if q'. The biconditional is False exactly "
        "when p and q differ."
    ),
    tier=1, domain="logic",
    source="Wikipedia contributors, 'Logical biconditional', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logical_biconditional",
    prerequisites=["implication"],
))

register_atom(Atom(
    atom_type="definition",
    name="syllogism",
    content=(
        "A syllogism is a deductive argument with two premises and one "
        "conclusion. The most common form (Barbara): All M are P; All S are "
        "M; therefore All S are P. Example: All mammals are animals; all "
        "dogs are mammals; therefore all dogs are animals. A syllogism is "
        "valid if the conclusion follows necessarily from the premises, "
        "regardless of whether the premises are actually true."
    ),
    tier=1, domain="logic",
    source="Wikipedia contributors, 'Syllogism', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Syllogism",
    prerequisites=["implication"],
))

# ── Tier 2 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="propositional_eval",
    content=(
        "Propositional logic formulas are built from variables, NOT, AND, "
        "OR, ->, and <->. Evaluation proceeds by: (1) substitute truth "
        "values for all variables, (2) evaluate innermost parentheses first, "
        "(3) apply precedence: NOT > AND > OR > -> > <->. A formula is a "
        "tautology if it evaluates to True for all possible inputs."
    ),
    tier=2, domain="logic",
    source="Wikipedia contributors, 'Propositional calculus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Propositional_calculus",
    prerequisites=["boolean_eval", "implication"],
))

register_atom(Atom(
    atom_type="theorem",
    name="logical_equivalence",
    content=(
        "Two formulas are logically equivalent if they produce the same "
        "truth value for every assignment of variables. Key equivalences: "
        "p -> q = NOT p OR q; "
        "NOT (p AND q) = NOT p OR NOT q (De Morgan); "
        "NOT (p OR q) = NOT p AND NOT q (De Morgan); "
        "p -> q = NOT q -> NOT p (contrapositive); "
        "p <-> q = (p -> q) AND (q -> p)."
    ),
    tier=2, domain="logic",
    source="Wikipedia contributors, 'Logical equivalence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Logical_equivalence",
    prerequisites=["propositional_eval"],
))

register_atom(Atom(
    atom_type="theorem",
    name="contrapositive",
    content=(
        "The contrapositive of the statement p -> q is NOT q -> NOT p. "
        "A conditional and its contrapositive are always logically "
        "equivalent. The converse (q -> p) and inverse (NOT p -> NOT q) "
        "are equivalent to each other but NOT equivalent to the original. "
        "This is a fundamental tool in proof by contradiction."
    ),
    tier=2, domain="logic",
    source="Wikipedia contributors, 'Contraposition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Contraposition",
    prerequisites=["implication"],
))

# ── Tier 3 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="deduction_chain",
    content=(
        "Deduction (modus ponens) states: if p -> q is true and p is true, "
        "then q is true. A deduction chain applies this rule repeatedly: "
        "given p -> q, q -> r, r -> s, and p, we derive q, then r, then s. "
        "Modus tollens is the contrapositive form: if p -> q and NOT q, "
        "then NOT p."
    ),
    tier=3, domain="logic",
    source="Wikipedia contributors, 'Modus ponens', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Modus_ponens",
    prerequisites=["propositional_eval", "contrapositive"],
))

register_atom(Atom(
    atom_type="definition",
    name="quantifier_eval",
    content=(
        "Universal quantifier (forall x, P(x)) asserts P holds for every "
        "element in the domain. Existential quantifier (exists x, P(x)) "
        "asserts P holds for at least one element. Negation: "
        "NOT (forall x, P(x)) = exists x, NOT P(x); "
        "NOT (exists x, P(x)) = forall x, NOT P(x). "
        "Evaluation over a finite domain checks each element."
    ),
    tier=3, domain="logic",
    source="Wikipedia contributors, 'Quantifier (logic)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Quantifier_(logic)",
    prerequisites=["negation", "propositional_eval"],
))

# ── Tier 4 ─────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="knights_knaves",
    content=(
        "In knights and knaves puzzles, inhabitants of an island are either "
        "knights (always tell the truth) or knaves (always lie). Given "
        "statements by inhabitants, determine who is a knight and who is a "
        "knave. The solving technique: assume each person's type and check "
        "consistency. If A says 'I am a knight', both knights and knaves "
        "would say this (it is not informative). If A says 'B is a knave', "
        "then if A is a knight, B must be a knave; if A is a knave, B must "
        "be a knight."
    ),
    tier=4, domain="logic",
    source="Wikipedia contributors, 'Knights and Knaves', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Knights_and_Knaves",
    prerequisites=["deduction_chain"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="logical_puzzle",
    content=(
        "Constraint satisfaction puzzles (e.g., Einstein's riddle) assign "
        "values to variables subject to constraints. Solving strategy: "
        "(1) list all constraints, (2) eliminate impossible assignments, "
        "(3) propagate forced assignments, (4) if stuck, branch on a choice "
        "and check consistency. A valid solution satisfies all constraints "
        "simultaneously."
    ),
    tier=4, domain="logic",
    source="Wikipedia contributors, 'Constraint satisfaction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Constraint_satisfaction",
    prerequisites=["deduction_chain"],
))
