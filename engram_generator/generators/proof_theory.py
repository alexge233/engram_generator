"""Proof theory generators.

6 generators across tiers 6-8 covering natural deduction, sequent
calculus, resolution refutation, Horn clauses, modal logic, and
intuitionistic logic.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Helper utilities ──────────────────────────────────────────────


class KripkeModel:
    """A Kripke model for modal logic evaluation.

    Holds a set of worlds, an accessibility relation, and a valuation
    mapping each world to a set of propositional variables that are true.

    Attributes:
        worlds: List of world names.
        access: Set of (world, world) pairs for accessibility.
        valuation: Mapping from world to set of true variables.
    """

    def __init__(self, worlds: list[str],
                 access: set[tuple[str, str]],
                 valuation: dict[str, set[str]]) -> None:
        """Initialise the Kripke model.

        Args:
            worlds: List of world names.
            access: Set of (w1, w2) accessibility pairs.
            valuation: Maps each world to its true variables.
        """
        self.worlds = worlds
        self.access = access
        self.valuation = valuation

    def accessible(self, w: str) -> list[str]:
        """Return worlds accessible from w.

        Args:
            w: Source world.

        Returns:
            List of accessible worlds.
        """
        return [w2 for (w1, w2) in self.access if w1 == w]

    def holds(self, w: str, var: str) -> bool:
        """Check if a propositional variable holds at world w.

        Args:
            w: World name.
            var: Variable name.

        Returns:
            True if var is true at w.
        """
        return var in self.valuation.get(w, set())

    def box(self, w: str, var: str) -> bool:
        """Evaluate Box(var) at world w.

        Box(p) is true at w iff p is true at all accessible worlds.

        Args:
            w: World name.
            var: Variable name.

        Returns:
            True if var holds at all accessible worlds.
        """
        reachable = self.accessible(w)
        if not reachable:
            return True  # vacuously true
        return all(self.holds(w2, var) for w2 in reachable)

    def diamond(self, w: str, var: str) -> bool:
        """Evaluate Diamond(var) at world w.

        Diamond(p) is true at w iff p is true at some accessible world.

        Args:
            w: World name.
            var: Variable name.

        Returns:
            True if var holds at some accessible world.
        """
        return any(self.holds(w2, var) for w2 in self.accessible(w))

    def __str__(self) -> str:
        """Return a compact string representation."""
        acc_str = ", ".join(
            f"{a}->{b}" for a, b in sorted(self.access)
        )
        val_str = "; ".join(
            f"{w}:{{{', '.join(sorted(vs))}}}"
            for w, vs in sorted(self.valuation.items())
        )
        return f"W={{{', '.join(self.worlds)}}}, R={{{acc_str}}}, V={{{val_str}}}"


# ── TIER 6 ────────────────────────────────────────────────────────


@register
class ResolutionRefutationGenerator(StepGenerator):
    """Prove unsatisfiability by resolution refutation.

    Negate the conclusion, convert premises and negated conclusion to
    CNF clauses, then repeatedly resolve pairs until the empty clause
    is derived (or no resolution is possible).

    Difficulty scaling:
        Difficulty 1-3: 2-3 clauses, 2 variables.
        Difficulty 4-6: 3-4 clauses, 3 variables.
        Difficulty 7-8: 4-5 clauses, 3-4 variables.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "resolution_refutation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sat_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove unsatisfiability by resolution refutation"

    def _resolve(self, c1: frozenset[str],
                 c2: frozenset[str]) -> frozenset[str] | None:
        """Attempt to resolve two clauses on a complementary literal.

        Args:
            c1: First clause as frozenset of literals.
            c2: Second clause as frozenset of literals.

        Returns:
            Resolvent clause, or None if no resolution possible.
        """
        for lit in c1:
            neg = f"~{lit}" if not lit.startswith("~") else lit[1:]
            if neg in c2:
                resolvent = (c1 - {lit}) | (c2 - {neg})
                return frozenset(resolvent)
        return None

    def _format_clause(self, clause: frozenset[str]) -> str:
        """Format a clause as a readable string.

        Args:
            clause: Frozenset of literals.

        Returns:
            String like '{p, ~q}' or '{}' for empty clause.
        """
        if not clause:
            return "{} (empty)"
        return "{" + ", ".join(sorted(clause)) + "}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a resolution refutation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Simple: {p}, {~p, q}, {~q} -> empty clause
            vars_used = self._rng.sample(["p", "q", "r", "s"], 2)
            a, b = vars_used
            clauses = [
                frozenset({a}),
                frozenset({f"~{a}", b}),
                frozenset({f"~{b}"}),
            ]
        elif difficulty <= 6:
            vars_used = self._rng.sample(["p", "q", "r", "s"], 3)
            a, b, c = vars_used
            clauses = [
                frozenset({a, b}),
                frozenset({f"~{a}"}),
                frozenset({f"~{b}", c}),
                frozenset({f"~{c}"}),
            ]
        else:
            vars_used = self._rng.sample(["p", "q", "r", "s"], 3)
            a, b, c = vars_used
            clauses = [
                frozenset({a}),
                frozenset({f"~{a}", b}),
                frozenset({f"~{a}", c}),
                frozenset({f"~{b}", f"~{c}"}),
                frozenset({a, f"~{c}"}),
            ]

        # Perform resolution to find derivation
        all_clauses = list(clauses)
        resolution_steps = []
        found_empty = False

        for i in range(len(all_clauses)):
            if found_empty:
                break
            for j in range(i + 1, len(all_clauses)):
                resolvent = self._resolve(all_clauses[i], all_clauses[j])
                if resolvent is not None and resolvent not in all_clauses:
                    step_desc = (
                        f"resolve {self._format_clause(all_clauses[i])} "
                        f"and {self._format_clause(all_clauses[j])} "
                        f"-> {self._format_clause(resolvent)}"
                    )
                    resolution_steps.append(step_desc)
                    all_clauses.append(resolvent)
                    if not resolvent:
                        found_empty = True
                        break

        clauses_str = ", ".join(
            self._format_clause(c) for c in clauses
        )
        return (
            f"Clauses: {clauses_str}. "
            f"Derive empty clause by resolution.",
            {"clauses": clauses_str,
             "resolution_steps": resolution_steps,
             "unsatisfiable": found_empty},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the resolution chain.
        """
        steps = [f"initial clauses: {sd['clauses']}"]
        steps.extend(sd["resolution_steps"])
        if sd["unsatisfiable"]:
            steps.append("empty clause derived: unsatisfiable")
        else:
            steps.append("no empty clause: satisfiable")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the satisfiability verdict.

        Args:
            sd: Solution data dict.

        Returns:
            'unsatisfiable' or 'satisfiable'.
        """
        return "unsatisfiable" if sd["unsatisfiable"] else "satisfiable"


@register
class HornClauseGenerator(StepGenerator):
    """Evaluate a Horn clause program using SLD resolution.

    Given a set of facts and rules (Horn clauses), determine if a
    query can be derived. Uses forward chaining: apply rules whose
    body is satisfied until the query is derived or no new facts appear.

    Difficulty scaling:
        Difficulty 1-3: 2-3 facts, 1-2 rules, simple query.
        Difficulty 4-6: 3-4 facts, 2-3 rules.
        Difficulty 7-8: 4-5 facts, 3-4 rules, chain reasoning.
    """

    _PREDICATES = ["parent", "ancestor", "human", "mortal",
                   "teacher", "wise", "even", "positive"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "horn_clause"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "evaluate Horn clause program"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Horn clause evaluation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        entities = self._rng.sample(
            ["alice", "bob", "carol", "dave", "eve"], 3
        )

        if difficulty <= 3:
            facts = [
                f"human({entities[0]})",
                f"human({entities[1]})",
            ]
            rules = [
                f"human(X) -> mortal(X)",
            ]
            query = f"mortal({entities[0]})"
            derivable = True
            derivation = [
                f"fact: human({entities[0]})",
                f"rule: human(X)->mortal(X), X={entities[0]}",
                f"derive: mortal({entities[0]})",
            ]
        elif difficulty <= 6:
            facts = [
                f"parent({entities[0]},{entities[1]})",
                f"parent({entities[1]},{entities[2]})",
                f"human({entities[0]})",
            ]
            rules = [
                "parent(X,Y) -> ancestor(X,Y)",
                "parent(X,Y) AND ancestor(Y,Z) -> ancestor(X,Z)",
            ]
            query = f"ancestor({entities[0]},{entities[2]})"
            derivable = True
            derivation = [
                f"fact: parent({entities[1]},{entities[2]})",
                f"rule 1: derive ancestor({entities[1]},{entities[2]})",
                f"fact: parent({entities[0]},{entities[1]})",
                f"rule 2: parent({entities[0]},{entities[1]}) AND "
                f"ancestor({entities[1]},{entities[2]}) -> "
                f"ancestor({entities[0]},{entities[2]})",
            ]
        else:
            facts = [
                f"parent({entities[0]},{entities[1]})",
                f"parent({entities[1]},{entities[2]})",
                f"human({entities[0]})",
                f"human({entities[1]})",
                f"human({entities[2]})",
            ]
            rules = [
                "parent(X,Y) -> ancestor(X,Y)",
                "parent(X,Y) AND ancestor(Y,Z) -> ancestor(X,Z)",
                "human(X) -> mortal(X)",
            ]
            # Query something not derivable
            query_type = self._rng.choice(["yes", "no"])
            if query_type == "yes":
                query = f"mortal({entities[2]})"
                derivable = True
                derivation = [
                    f"fact: human({entities[2]})",
                    f"rule: human(X)->mortal(X), X={entities[2]}",
                    f"derive: mortal({entities[2]})",
                ]
            else:
                query = f"ancestor({entities[2]},{entities[0]})"
                derivable = False
                derivation = [
                    f"no fact parent({entities[2]},_) exists",
                    f"cannot derive ancestor({entities[2]},{entities[0]})",
                    "forward chaining exhausted, query not derived",
                ]

        facts_str = "; ".join(facts)
        rules_str = "; ".join(rules)
        return (
            f"Facts: {facts_str}. Rules: {rules_str}. "
            f"Query: {query}?",
            {"facts": facts, "rules": rules, "query": query,
             "derivable": derivable, "derivation": derivation},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing SLD resolution derivation.
        """
        return sd["derivation"]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the query is derivable.

        Args:
            sd: Solution data dict.

        Returns:
            'YES' or 'NO'.
        """
        return "YES" if sd["derivable"] else "NO"


# ── TIER 7 ────────────────────────────────────────────────────────


@register
class NaturalDeductionGenerator(StepGenerator):
    """Derive a conclusion using natural deduction rules.

    Apply rules including ->I (implication introduction), ->E (modus
    ponens), ^I/^E (conjunction intro/elim), vI/vE (disjunction
    intro/elim), ~I/~E (negation intro/elim) to build a derivation.

    Difficulty scaling:
        Difficulty 1-3: 1-2 rule applications (modus ponens).
        Difficulty 4-6: 2-3 rule applications (conjunction, disjunction).
        Difficulty 7-8: 3-4 rule applications (nested assumptions).
    """

    _DERIVATIONS = [
        {
            "premises": ["p", "p -> q"],
            "conclusion": "q",
            "rules": ["->E"],
            "steps": [
                "1. p (premise)",
                "2. p -> q (premise)",
                "3. q (->E on 1, 2)",
            ],
        },
        {
            "premises": ["p", "q"],
            "conclusion": "p ^ q",
            "rules": ["^I"],
            "steps": [
                "1. p (premise)",
                "2. q (premise)",
                "3. p ^ q (^I on 1, 2)",
            ],
        },
        {
            "premises": ["p ^ q"],
            "conclusion": "p",
            "rules": ["^E"],
            "steps": [
                "1. p ^ q (premise)",
                "2. p (^E on 1)",
            ],
        },
        {
            "premises": ["p"],
            "conclusion": "p v q",
            "rules": ["vI"],
            "steps": [
                "1. p (premise)",
                "2. p v q (vI on 1)",
            ],
        },
        {
            "premises": ["p -> q", "q -> r", "p"],
            "conclusion": "r",
            "rules": ["->E", "->E"],
            "steps": [
                "1. p (premise)",
                "2. p -> q (premise)",
                "3. q (->E on 1, 2)",
                "4. q -> r (premise)",
                "5. r (->E on 3, 4)",
            ],
        },
        {
            "premises": ["p -> q", "~q"],
            "conclusion": "~p",
            "rules": ["~I"],
            "steps": [
                "1. p -> q (premise)",
                "2. ~q (premise)",
                "3. [assume p]",
                "4. q (->E on 3, 1)",
                "5. contradiction (q, ~q)",
                "6. ~p (~I, discharging 3)",
            ],
        },
        {
            "premises": ["p v q", "p -> r", "q -> r"],
            "conclusion": "r",
            "rules": ["vE"],
            "steps": [
                "1. p v q (premise)",
                "2. [assume p] -> r (by p -> r)",
                "3. [assume q] -> r (by q -> r)",
                "4. r (vE on 1, 2, 3)",
            ],
        },
        {
            "premises": ["p ^ q", "q -> r"],
            "conclusion": "p ^ r",
            "rules": ["^E", "->E", "^I"],
            "steps": [
                "1. p ^ q (premise)",
                "2. p (^E on 1)",
                "3. q (^E on 1)",
                "4. q -> r (premise)",
                "5. r (->E on 3, 4)",
                "6. p ^ r (^I on 2, 5)",
            ],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "natural_deduction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["deduction_chain"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "derive conclusion using natural deduction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a natural deduction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._DERIVATIONS[:4]
        elif difficulty <= 6:
            pool = self._DERIVATIONS[:6]
        else:
            pool = self._DERIVATIONS

        deriv = self._rng.choice(pool)

        # Randomise variable names
        var_map = {}
        available = self._rng.sample(
            ["p", "q", "r", "s", "t", "u"], 4
        )
        for i, orig in enumerate(["p", "q", "r", "s"]):
            var_map[orig] = available[i]

        def rename(text: str) -> str:
            """Rename variables in a formula string."""
            result = text
            # Replace in reverse length order to avoid partial matches
            for orig, new in sorted(var_map.items(),
                                     key=lambda x: -len(x[0])):
                result = result.replace(orig, new)
            return result

        premises = [rename(p) for p in deriv["premises"]]
        conclusion = rename(deriv["conclusion"])
        steps = [rename(s) for s in deriv["steps"]]
        rules = deriv["rules"]

        premises_str = ", ".join(premises)
        return (
            f"Premises: {premises_str}. "
            f"Derive: {conclusion}.",
            {"premises": premises, "conclusion": conclusion,
             "rules": rules, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the natural deduction derivation.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the derived conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            The conclusion formula.
        """
        return sd["conclusion"]


@register
class ModalLogicGenerator(StepGenerator):
    """Evaluate a modal formula in a Kripke model.

    Given a Kripke model (worlds, accessibility relation, valuation)
    and a modal formula involving Box and Diamond, evaluate the formula
    at a specified world.

    Difficulty scaling:
        Difficulty 1-3: 2 worlds, single Box or Diamond.
        Difficulty 4-6: 3 worlds, Box/Diamond combinations.
        Difficulty 7-8: 3-4 worlds, nested modalities.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "modal_logic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["propositional_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "evaluate modal formula in Kripke model"

    def _build_model(self, difficulty: int) -> KripkeModel:
        """Build a random Kripke model scaled to difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A KripkeModel instance.
        """
        if difficulty <= 3:
            n_worlds = 2
        elif difficulty <= 6:
            n_worlds = 3
        else:
            n_worlds = self._rng.randint(3, 4)

        worlds = [f"w{i}" for i in range(n_worlds)]
        access: set[tuple[str, str]] = set()
        for w1 in worlds:
            for w2 in worlds:
                if self._rng.random() < 0.4:
                    access.add((w1, w2))

        variables = self._rng.sample(["p", "q", "r"], 2)
        valuation: dict[str, set[str]] = {}
        for w in worlds:
            true_vars: set[str] = set()
            for v in variables:
                if self._rng.random() < 0.5:
                    true_vars.add(v)
            valuation[w] = true_vars

        return KripkeModel(worlds, access, valuation)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a modal logic evaluation problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        model = self._build_model(difficulty)
        eval_world = self._rng.choice(model.worlds)
        var = self._rng.choice(
            sorted(
                set().union(*(model.valuation[w] for w in model.worlds))
                or {"p"}
            )
        )

        if difficulty <= 3:
            modality = self._rng.choice(["Box", "Diamond"])
        elif difficulty <= 6:
            modality = self._rng.choice(
                ["Box", "Diamond", "Box NOT", "Diamond NOT"]
            )
        else:
            modality = self._rng.choice(
                ["Box", "Diamond", "NOT Box", "NOT Diamond",
                 "Box Box", "Diamond Diamond"]
            )

        # Evaluate the formula
        accessible = model.accessible(eval_world)
        acc_str = ", ".join(accessible) if accessible else "none"

        if modality == "Box":
            result = model.box(eval_world, var)
            check = " AND ".join(
                f"{var}@{w2}={model.holds(w2, var)}"
                for w2 in accessible
            ) if accessible else "vacuously true"
        elif modality == "Diamond":
            result = model.diamond(eval_world, var)
            check = " OR ".join(
                f"{var}@{w2}={model.holds(w2, var)}"
                for w2 in accessible
            ) if accessible else "false (no accessible worlds)"
        elif modality == "Box NOT":
            result = all(
                not model.holds(w2, var) for w2 in accessible
            ) if accessible else True
            check = " AND ".join(
                f"~{var}@{w2}={not model.holds(w2, var)}"
                for w2 in accessible
            ) if accessible else "vacuously true"
        elif modality == "Diamond NOT":
            result = any(
                not model.holds(w2, var) for w2 in accessible
            ) if accessible else False
            check = " OR ".join(
                f"~{var}@{w2}={not model.holds(w2, var)}"
                for w2 in accessible
            ) if accessible else "false"
        elif modality == "NOT Box":
            result = not model.box(eval_world, var)
            check = f"NOT (Box {var}) = NOT {model.box(eval_world, var)}"
        elif modality == "NOT Diamond":
            result = not model.diamond(eval_world, var)
            check = (f"NOT (Diamond {var}) = "
                     f"NOT {model.diamond(eval_world, var)}")
        elif modality == "Box Box":
            # Box(Box p) at w: for all w' accessible from w,
            # Box p holds at w'
            result = all(
                model.box(w2, var) for w2 in accessible
            ) if accessible else True
            check = " AND ".join(
                f"Box({var})@{w2}={model.box(w2, var)}"
                for w2 in accessible
            ) if accessible else "vacuously true"
        else:  # Diamond Diamond
            result = any(
                model.diamond(w2, var) for w2 in accessible
            ) if accessible else False
            check = " OR ".join(
                f"Diamond({var})@{w2}={model.diamond(w2, var)}"
                for w2 in accessible
            ) if accessible else "false"

        formula = f"{modality} {var}"
        return (
            f"Kripke model: {model}. "
            f"Evaluate '{formula}' at {eval_world}.",
            {"model": str(model), "world": eval_world,
             "formula": formula, "accessible": acc_str,
             "check": check, "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the modal evaluation.
        """
        return [
            f"model: {sd['model']}",
            f"evaluate '{sd['formula']}' at {sd['world']}",
            f"accessible worlds: {sd['accessible']}",
            f"check: {sd['check']}",
            f"result: {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the truth value.

        Args:
            sd: Solution data dict.

        Returns:
            'True' or 'False'.
        """
        return str(sd["result"])


@register
class IntuitionisticLogicGenerator(StepGenerator):
    """Identify classical tautologies that fail intuitionistically.

    Present a formula and determine whether it is valid in intuitionistic
    logic. Classical tautologies like excluded middle (p v ~p), double
    negation elimination (~~p -> p), and Peirce's law
    (((p->q)->p)->p) are not intuitionistically valid.

    Difficulty scaling:
        Difficulty 1-3: basic formulas with clear classification.
        Difficulty 4-6: mix of valid and invalid formulas.
        Difficulty 7-8: subtler formulas requiring justification.
    """

    _FORMULAS = [
        {
            "formula": "p v ~p",
            "name": "excluded middle",
            "classical": True,
            "intuitionistic": False,
            "reason": "no constructive proof of p or ~p in general",
        },
        {
            "formula": "~~p -> p",
            "name": "double negation elimination",
            "classical": True,
            "intuitionistic": False,
            "reason": "knowing ~~p does not constructively yield p",
        },
        {
            "formula": "((p -> q) -> p) -> p",
            "name": "Peirce's law",
            "classical": True,
            "intuitionistic": False,
            "reason": "requires excluded middle in its proof",
        },
        {
            "formula": "p -> ~~p",
            "name": "double negation introduction",
            "classical": True,
            "intuitionistic": True,
            "reason": "constructively valid: given p, assume ~p, "
                      "derive contradiction",
        },
        {
            "formula": "p -> p",
            "name": "identity",
            "classical": True,
            "intuitionistic": True,
            "reason": "trivially constructive: given p, return p",
        },
        {
            "formula": "(p ^ q) -> p",
            "name": "conjunction elimination",
            "classical": True,
            "intuitionistic": True,
            "reason": "constructively valid: extract first component",
        },
        {
            "formula": "~(p ^ ~p)",
            "name": "non-contradiction",
            "classical": True,
            "intuitionistic": True,
            "reason": "assume p ^ ~p, derive contradiction, "
                      "apply ~I",
        },
        {
            "formula": "(p -> q) -> (~q -> ~p)",
            "name": "contrapositive",
            "classical": True,
            "intuitionistic": True,
            "reason": "constructively valid via composition",
        },
        {
            "formula": "~p v ~~p",
            "name": "weak excluded middle variant",
            "classical": True,
            "intuitionistic": False,
            "reason": "instance of excluded middle on ~p",
        },
        {
            "formula": "(~p -> p) -> p",
            "name": "consequentia mirabilis",
            "classical": True,
            "intuitionistic": False,
            "reason": "equivalent to excluded middle",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "intuitionistic_logic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_deduction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify formula as intuitionistically valid or not"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an intuitionistic logic classification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(4 + difficulty, len(self._FORMULAS))
        formula_data = self._rng.choice(self._FORMULAS[:pool_size])

        return (
            f"Is '{formula_data['formula']}' "
            f"({formula_data['name']}) valid in intuitionistic logic?",
            formula_data,
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the classification reasoning.
        """
        return [
            f"formula: {sd['formula']} ({sd['name']})",
            f"classically valid: {sd['classical']}",
            f"intuitionistically valid: {sd['intuitionistic']}",
            f"reason: {sd['reason']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the intuitionistic validity.

        Args:
            sd: Solution data dict.

        Returns:
            'intuitionistically valid' or 'NOT intuitionistically valid'.
        """
        if sd["intuitionistic"]:
            return "intuitionistically valid"
        return "NOT intuitionistically valid"


# ── TIER 8 ────────────────────────────────────────────────────────


@register
class SequentCalculusGenerator(StepGenerator):
    """Apply structural rules to sequent calculus proofs.

    Given a sequent (Gamma |- Delta), apply rules such as weakening,
    contraction, and cut to transform it. Show the proof transformation
    step by step.

    Difficulty scaling:
        Difficulty 1-3: single rule application (weakening).
        Difficulty 4-6: two rules (weakening + contraction).
        Difficulty 7-8: cut rule with two premise sequents.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sequent_calculus"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_deduction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply structural rules to sequent"

    def _format_sequent(self, gamma: list[str],
                        delta: list[str]) -> str:
        """Format a sequent as 'A, B |- C, D'.

        Args:
            gamma: Left side formulas.
            delta: Right side formulas.

        Returns:
            Formatted sequent string.
        """
        left = ", ".join(gamma) if gamma else ""
        right = ", ".join(delta) if delta else ""
        return f"{left} |- {right}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequent calculus problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vars_pool = self._rng.sample(
            ["A", "B", "C", "D", "E", "F"], 4
        )

        if difficulty <= 3:
            # Weakening: add a formula to an existing sequent
            gamma = [vars_pool[0]]
            delta = [vars_pool[1]]
            rule = "weakening"
            added = vars_pool[2]
            side = self._rng.choice(["left", "right"])
            if side == "left":
                result_gamma = [vars_pool[0], added]
                result_delta = list(delta)
            else:
                result_gamma = list(gamma)
                result_delta = [vars_pool[1], added]

            original = self._format_sequent(gamma, delta)
            result = self._format_sequent(result_gamma, result_delta)
            steps = [
                f"sequent: {original}",
                f"apply {side}-weakening with {added}",
                f"result: {result}",
            ]

        elif difficulty <= 6:
            # Contraction: merge duplicate formula
            gamma = [vars_pool[0], vars_pool[0], vars_pool[1]]
            delta = [vars_pool[2]]
            rule = "contraction"
            result_gamma = [vars_pool[0], vars_pool[1]]
            result_delta = list(delta)

            original = self._format_sequent(gamma, delta)
            result = self._format_sequent(result_gamma, result_delta)
            steps = [
                f"sequent: {original}",
                f"left-contraction on {vars_pool[0]}",
                f"result: {result}",
            ]

        else:
            # Cut: given Gamma |- A, Delta and A, Sigma |- Pi,
            # derive Gamma, Sigma |- Delta, Pi
            rule = "cut"
            cut_formula = vars_pool[0]
            gamma1 = [vars_pool[1]]
            delta1 = [cut_formula, vars_pool[2]]
            gamma2 = [cut_formula, vars_pool[3]]
            delta2 = [vars_pool[2]]

            result_gamma = [vars_pool[1], vars_pool[3]]
            result_delta = [vars_pool[2], vars_pool[2]]

            seq1 = self._format_sequent(gamma1, delta1)
            seq2 = self._format_sequent(gamma2, delta2)
            result = self._format_sequent(result_gamma, result_delta)
            original = f"{seq1} and {seq2}"
            steps = [
                f"sequent 1: {seq1}",
                f"sequent 2: {seq2}",
                f"cut on {cut_formula}",
                f"result: {result}",
            ]

        return (
            f"Sequent: {original}. Apply {rule}.",
            {"original": original, "rule": rule,
             "result": result, "steps": steps},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the structural rule application.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the resulting sequent.

        Args:
            sd: Solution data dict.

        Returns:
            The transformed sequent.
        """
        return sd["result"]
