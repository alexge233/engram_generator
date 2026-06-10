"""Model theory generators.

5 generators across tiers 7-8 covering structure checking,
elementary equivalence, compactness, ultraproducts, and definability.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── Helper utilities ──────────────────────────────────────────────


class FiniteStructure:
    """A finite first-order structure with domain and interpretations.

    Holds a domain of elements, relation interpretations (sets of tuples),
    and constant interpretations (single elements).

    Attributes:
        domain: List of domain elements.
        relations: Mapping from relation name to set of tuples.
        constants: Mapping from constant name to domain element.
    """

    def __init__(self, domain: list[int],
                 relations: dict[str, set[tuple[int, ...]]],
                 constants: dict[str, int]) -> None:
        """Initialise the structure.

        Args:
            domain: List of domain elements.
            relations: Mapping from relation name to set of tuples.
            constants: Mapping from constant name to domain element.
        """
        self.domain = domain
        self.relations = relations
        self.constants = constants

    def __str__(self) -> str:
        """Return a compact string representation."""
        rels = ", ".join(
            f"{k}={{{', '.join(str(t) for t in sorted(v))}}}"
            for k, v in sorted(self.relations.items())
        )
        consts = ", ".join(
            f"{k}={v}" for k, v in sorted(self.constants.items())
        )
        parts = [f"D={{{', '.join(str(d) for d in self.domain)}}}"]
        if rels:
            parts.append(rels)
        if consts:
            parts.append(consts)
        return "; ".join(parts)


class SentenceTemplate:
    """A first-order sentence template with evaluator.

    Represents a sentence pattern like 'forall x: R(x,x)' together
    with a callable that evaluates it over a FiniteStructure.

    Attributes:
        text: Human-readable sentence string.
        evaluator: Callable taking a FiniteStructure and returning bool.
    """

    def __init__(self, text: str,
                 evaluator: "callable") -> None:
        """Initialise the template.

        Args:
            text: Human-readable sentence string.
            evaluator: Function from FiniteStructure to bool.
        """
        self.text = text
        self.evaluator = evaluator

    def evaluate(self, structure: "FiniteStructure") -> bool:
        """Evaluate the sentence on a structure.

        Args:
            structure: The finite structure to evaluate on.

        Returns:
            True if the structure satisfies the sentence.
        """
        return self.evaluator(structure)


def _reflexive(s: FiniteStructure) -> bool:
    """Check if R is reflexive on s."""
    return all((x, x) in s.relations.get("R", set()) for x in s.domain)


def _symmetric(s: FiniteStructure) -> bool:
    """Check if R is symmetric on s."""
    r = s.relations.get("R", set())
    return all((b, a) in r for (a, b) in r)


def _transitive(s: FiniteStructure) -> bool:
    """Check if R is transitive on s."""
    r = s.relations.get("R", set())
    return all(
        (a, c) in r
        for (a, b) in r
        for (b2, c) in r
        if b == b2
    )


def _total(s: FiniteStructure) -> bool:
    """Check if R is total (forall x exists y: R(x,y))."""
    r = s.relations.get("R", set())
    return all(any((x, y) in r for y in s.domain) for x in s.domain)


def _exists_fixed(s: FiniteStructure) -> bool:
    """Check if exists x: R(x,x)."""
    r = s.relations.get("R", set())
    return any((x, x) in r for x in s.domain)


_SENTENCE_POOL = [
    SentenceTemplate("forall x: R(x,x)", _reflexive),
    SentenceTemplate("forall x,y: R(x,y)->R(y,x)", _symmetric),
    SentenceTemplate("forall x,y,z: R(x,y)&R(y,z)->R(x,z)", _transitive),
    SentenceTemplate("forall x exists y: R(x,y)", _total),
    SentenceTemplate("exists x: R(x,x)", _exists_fixed),
]


# ── TIER 7 ────────────────────────────────────────────────────────


@register
class StructureCheckGenerator(StepGenerator):
    """Determine if a finite structure satisfies a first-order sentence.

    Given a finite domain with a binary relation R and a sentence such as
    'forall x: R(x,x)', evaluate the sentence on every relevant tuple.

    Difficulty scaling:
        Difficulty 1-3: domain size 2-3, simple sentences.
        Difficulty 4-6: domain size 3-4, broader sentence pool.
        Difficulty 7-8: domain size 4-5, full sentence pool.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "structure_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantifier_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check if structure satisfies first-order sentence"

    def _build_structure(self, difficulty: int) -> FiniteStructure:
        """Build a random finite structure scaled to difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A FiniteStructure with a binary relation R.
        """
        if difficulty <= 3:
            size = self._rng.randint(2, 3)
        elif difficulty <= 6:
            size = self._rng.randint(3, 4)
        else:
            size = self._rng.randint(4, 5)

        domain = list(range(1, size + 1))
        pairs: set[tuple[int, int]] = set()
        for a in domain:
            for b in domain:
                if self._rng.random() < 0.4:
                    pairs.add((a, b))
        return FiniteStructure(domain, {"R": pairs}, {})

    def _pick_sentence(self, difficulty: int) -> SentenceTemplate:
        """Pick a sentence template appropriate for difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            A SentenceTemplate instance.
        """
        pool_size = min(2 + difficulty, len(_SENTENCE_POOL))
        return self._rng.choice(_SENTENCE_POOL[:pool_size])

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a structure checking problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        structure = self._build_structure(difficulty)
        sentence = self._pick_sentence(difficulty)
        result = sentence.evaluate(structure)

        return (
            f"Structure: {structure}. "
            f"Does it satisfy '{sentence.text}'?",
            {"structure": str(structure), "sentence": sentence.text,
             "result": result},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing evaluation.
        """
        return [
            f"structure: {sd['structure']}",
            f"sentence: {sd['sentence']}",
            f"evaluate on all relevant tuples",
            f"result: {sd['result']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return whether the sentence is satisfied.

        Args:
            sd: Solution data dict.

        Returns:
            'True' or 'False'.
        """
        return str(sd["result"])


@register
class ElementaryEquivalenceGenerator(StepGenerator):
    """Check if two finite structures satisfy the same set of sentences.

    Given two structures with binary relation R and 3-5 first-order
    sentences, evaluate each sentence on both structures. The structures
    are elementarily equivalent (w.r.t. the given sentences) if they
    agree on all of them.

    Difficulty scaling:
        Difficulty 1-3: domain size 2, 3 sentences.
        Difficulty 4-6: domain size 3, 4 sentences.
        Difficulty 7-8: domain size 3-4, 5 sentences.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "elementary_equivalence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["structure_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check elementary equivalence of two structures"

    def _build_structure(self, size: int) -> FiniteStructure:
        """Build a random finite structure of given size.

        Args:
            size: Number of domain elements.

        Returns:
            A FiniteStructure with binary relation R.
        """
        domain = list(range(1, size + 1))
        pairs: set[tuple[int, int]] = set()
        for a in domain:
            for b in domain:
                if self._rng.random() < 0.4:
                    pairs.add((a, b))
        return FiniteStructure(domain, {"R": pairs}, {})

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an elementary equivalence problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            size = 2
            n_sentences = 3
        elif difficulty <= 6:
            size = 3
            n_sentences = 4
        else:
            size = self._rng.randint(3, 4)
            n_sentences = 5

        s1 = self._build_structure(size)
        s2 = self._build_structure(size)

        sentences = self._rng.sample(
            _SENTENCE_POOL, min(n_sentences, len(_SENTENCE_POOL))
        )

        evaluations: list[dict] = []
        all_agree = True
        for sent in sentences:
            r1 = sent.evaluate(s1)
            r2 = sent.evaluate(s2)
            evaluations.append({
                "sentence": sent.text, "s1": r1, "s2": r2,
                "agree": r1 == r2,
            })
            if r1 != r2:
                all_agree = False

        return (
            f"A: {s1}. B: {s2}. "
            f"Sentences: {', '.join(s.text for s in sentences)}. "
            f"Do A and B agree on all?",
            {"s1": str(s1), "s2": str(s2),
             "evaluations": evaluations, "equivalent": all_agree},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing per-sentence evaluation.
        """
        steps = [f"A: {sd['s1']}", f"B: {sd['s2']}"]
        for ev in sd["evaluations"]:
            steps.append(
                f"{ev['sentence']}: A={ev['s1']}, B={ev['s2']}, "
                f"agree={ev['agree']}"
            )
        steps.append(f"equivalent: {sd['equivalent']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the structures are equivalent.

        Args:
            sd: Solution data dict.

        Returns:
            'True' or 'False'.
        """
        return str(sd["equivalent"])


@register
class DefinabilityGenerator(StepGenerator):
    """Check if a subset of the domain is definable by a first-order formula.

    Given a structure with binary relation R and a candidate formula
    phi(x), evaluate phi on each domain element to obtain the definable
    set, then compare with a target subset.

    Difficulty scaling:
        Difficulty 1-3: domain size 3, simple formulas.
        Difficulty 4-6: domain size 4, broader formula pool.
        Difficulty 7-8: domain size 5, full formula pool.
    """

    _FORMULAS = [
        ("R(x,x)", lambda s, x: (x, x) in s.relations.get("R", set())),
        ("exists y: R(x,y)",
         lambda s, x: any((x, y) in s.relations.get("R", set())
                          for y in s.domain)),
        ("exists y: R(y,x)",
         lambda s, x: any((y, x) in s.relations.get("R", set())
                          for y in s.domain)),
        ("forall y: R(x,y)",
         lambda s, x: all((x, y) in s.relations.get("R", set())
                          for y in s.domain)),
        ("NOT R(x,x)",
         lambda s, x: (x, x) not in s.relations.get("R", set())),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "definability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["quantifier_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check if subset is definable by first-order formula"

    def _build_structure(self, size: int) -> FiniteStructure:
        """Build a random finite structure of given size.

        Args:
            size: Number of domain elements.

        Returns:
            A FiniteStructure with binary relation R.
        """
        domain = list(range(1, size + 1))
        pairs: set[tuple[int, int]] = set()
        for a in domain:
            for b in domain:
                if self._rng.random() < 0.4:
                    pairs.add((a, b))
        return FiniteStructure(domain, {"R": pairs}, {})

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a definability problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            size = 3
        elif difficulty <= 6:
            size = 4
        else:
            size = 5

        structure = self._build_structure(size)
        pool_size = min(2 + difficulty, len(self._FORMULAS))
        formula_text, formula_fn = self._rng.choice(
            self._FORMULAS[:pool_size]
        )

        defined_set = {
            x for x in structure.domain
            if formula_fn(structure, x)
        }

        # With 50% chance, use the exact defined set as target;
        # otherwise, perturb it so the answer is False.
        if self._rng.random() < 0.5:
            target = defined_set
            matches = True
        else:
            target = set(defined_set)
            # Flip one element
            if target and self._rng.random() < 0.5:
                target.discard(self._rng.choice(list(target)))
            else:
                remaining = set(structure.domain) - target
                if remaining:
                    target.add(self._rng.choice(list(remaining)))
            matches = (target == defined_set)

        target_str = "{" + ", ".join(str(x) for x in sorted(target)) + "}"
        defined_str = "{" + ", ".join(
            str(x) for x in sorted(defined_set)
        ) + "}"

        evals = []
        for x in structure.domain:
            val = formula_fn(structure, x)
            evals.append(f"x={x}: {formula_text} = {val}")

        return (
            f"Structure: {structure}. "
            f"Formula phi(x): {formula_text}. "
            f"Target set: {target_str}. "
            f"Is target = {{x | phi(x)}}?",
            {"structure": str(structure), "formula": formula_text,
             "target": target_str, "defined": defined_str,
             "evals": evals, "matches": matches},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing per-element evaluation.
        """
        steps = sd["evals"]
        steps.append(f"defined set = {sd['defined']}")
        steps.append(f"target = {sd['target']}")
        steps.append(f"match: {sd['matches']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether target equals the defined set.

        Args:
            sd: Solution data dict.

        Returns:
            'True' or 'False'.
        """
        return str(sd["matches"])


# ── TIER 8 ────────────────────────────────────────────────────────


@register
class CompactnessApplyGenerator(StepGenerator):
    """Apply the compactness theorem to a finitely satisfiable set.

    Given a set of first-order sentences where every finite subset has a
    model, conclude by compactness that the entire set is consistent.
    Template-based: each problem presents a scenario and asks the student
    to identify why compactness applies.

    Difficulty scaling:
        Difficulty 1-3: 3 sentences, simple scenario.
        Difficulty 4-6: 4-5 sentences, richer scenario.
        Difficulty 7-8: 5-6 sentences, abstract scenario.
    """

    _SCENARIOS = [
        {
            "desc": "infinite graph coloring",
            "sentences": [
                "forall x: color(x)=R OR color(x)=B",
                "forall x,y: E(x,y) -> color(x)!=color(y)",
                "exists x: color(x)=R",
            ],
            "reason": "every finite subgraph is 2-colorable",
        },
        {
            "desc": "non-standard model of arithmetic",
            "sentences": [
                "forall x: S(x)!=0",
                "forall x,y: S(x)=S(y)->x=y",
                "c!=0", "c!=S(0)", "c!=S(S(0))",
            ],
            "reason": "every finite subset has a standard model "
                      "with c interpreted as a large enough number",
        },
        {
            "desc": "infinite linear order extension",
            "sentences": [
                "forall x: x<=x",
                "forall x,y: x<=y AND y<=x -> x=y",
                "forall x,y,z: x<=y AND y<=z -> x<=z",
                "forall x,y: x<=y OR y<=x",
            ],
            "reason": "every finite partial order extends to a "
                      "finite linear order",
        },
        {
            "desc": "type realization in an infinite structure",
            "sentences": [
                "exists x: P(x)",
                "exists x: NOT P(x)",
                "forall x: P(x)->Q(x)",
                "exists x: Q(x) AND NOT P(x)",
                "forall x exists y: R(x,y)",
            ],
            "reason": "each finite subset is satisfiable by choosing "
                      "a large enough domain with suitable predicates",
        },
        {
            "desc": "graph with arbitrarily long paths",
            "sentences": [
                "exists x0,x1: E(x0,x1) AND x0!=x1",
                "exists x0,x1,x2: E(x0,x1) AND E(x1,x2) "
                "AND x0!=x1 AND x1!=x2",
                "exists x0,x1,x2,x3: E(x0,x1) AND E(x1,x2) "
                "AND E(x2,x3) AND all distinct",
            ],
            "reason": "every finite subset only demands paths up "
                      "to a bounded length",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compactness_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["structure_check"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply compactness theorem to finitely satisfiable set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compactness theorem application problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(2 + difficulty // 2, len(self._SCENARIOS))
        scenario = self._rng.choice(self._SCENARIOS[:pool_size])

        if difficulty <= 3:
            n_show = min(3, len(scenario["sentences"]))
        elif difficulty <= 6:
            n_show = min(4, len(scenario["sentences"]))
        else:
            n_show = len(scenario["sentences"])

        shown = scenario["sentences"][:n_show]
        sent_str = "; ".join(shown)

        return (
            f"Scenario: {scenario['desc']}. "
            f"Sentences: {sent_str}. "
            f"Every finite subset has a model. Conclude?",
            {"desc": scenario["desc"], "sentences": shown,
             "reason": scenario["reason"],
             "n_sentences": n_show},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing compactness argument.
        """
        return [
            f"scenario: {sd['desc']}",
            f"sentence count: {sd['n_sentences']}",
            f"every finite subset is satisfiable because: {sd['reason']}",
            "by compactness: the entire set is consistent "
            "(has a model)",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the compactness conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            Statement that the set is consistent.
        """
        return "consistent (by compactness)"


@register
class UltraproductGenerator(StepGenerator):
    """Construct the ultraproduct of two finite structures.

    Given two structures A and B over the index set {0,1} with a
    principal ultrafilter containing {0} or {1}, compute the
    ultraproduct domain and the relation on it. Since the ultrafilter
    is principal, the ultraproduct is isomorphic to one factor.

    Difficulty scaling:
        Difficulty 1-3: domain size 2, ultrafilter on {0}.
        Difficulty 4-6: domain size 2-3, either ultrafilter.
        Difficulty 7-8: domain size 3, either ultrafilter, more pairs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ultraproduct"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["compactness_apply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "construct ultraproduct of two finite structures"

    def _build_structure(self, size: int) -> FiniteStructure:
        """Build a random finite structure of given size.

        Args:
            size: Number of domain elements.

        Returns:
            A FiniteStructure with binary relation R.
        """
        domain = list(range(1, size + 1))
        pairs: set[tuple[int, int]] = set()
        density = 0.35 if size <= 2 else 0.25
        for a in domain:
            for b in domain:
                if self._rng.random() < density:
                    pairs.add((a, b))
        return FiniteStructure(domain, {"R": pairs}, {})

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ultraproduct construction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            size = 2
            uf_index = 0
        elif difficulty <= 6:
            size = self._rng.randint(2, 3)
            uf_index = self._rng.choice([0, 1])
        else:
            size = 3
            uf_index = self._rng.choice([0, 1])

        s_a = self._build_structure(size)
        s_b = self._build_structure(size)
        structures = [s_a, s_b]

        # Principal ultrafilter on {uf_index} means the ultraproduct
        # is isomorphic to structures[uf_index].
        result_structure = structures[uf_index]
        uf_name = f"{{{uf_index}}}"

        r_sorted = sorted(result_structure.relations.get("R", set()))
        result_rel = "{" + ", ".join(str(t) for t in r_sorted) + "}"
        result_dom = (
            "{" + ", ".join(str(d) for d in result_structure.domain) + "}"
        )

        return (
            f"A: {s_a}. B: {s_b}. "
            f"Index set I={{0,1}}, ultrafilter U contains {uf_name}. "
            f"Compute ultraproduct domain and R.",
            {"s_a": str(s_a), "s_b": str(s_b),
             "uf_index": uf_index,
             "result_dom": result_dom,
             "result_rel": result_rel},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing ultraproduct construction.
        """
        return [
            f"A: {sd['s_a']}",
            f"B: {sd['s_b']}",
            f"ultrafilter U is principal on {{{sd['uf_index']}}}",
            f"ultraproduct isomorphic to "
            f"{'A' if sd['uf_index'] == 0 else 'B'}",
            f"domain = {sd['result_dom']}",
            f"R = {sd['result_rel']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the ultraproduct domain and relation.

        Args:
            sd: Solution data dict.

        Returns:
            Domain and relation as a string.
        """
        return f"domain={sd['result_dom']}, R={sd['result_rel']}"
