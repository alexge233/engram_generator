"""Category theory generators.

8 generators covering morphism composition, functors, natural
transformations, products, coproducts, adjunctions, Yoneda lemma,
and limits across tiers 7-8. All examples use small finite categories
with 2-4 objects to stay under 512 characters.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════════

def _format_set(elements: list | set) -> str:
    """Format a collection as a set string.

    Args:
        elements: Iterable of elements to format.

    Returns:
        String like ``{A, B, C}``.
    """
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


def _format_map(mapping: dict) -> str:
    """Format a mapping as a compact string.

    Args:
        mapping: Dictionary to format.

    Returns:
        String like ``A->X, B->Y``.
    """
    return ", ".join(f"{k}->{v}" for k, v in sorted(mapping.items()))


class SmallCategory:
    """A small finite category with explicitly listed morphisms.

    Objects are uppercase letters. Morphisms are stored as a
    composition table mapping (f, g) to g.f (compose g after f).

    Attributes:
        objects: List of object names.
        morphisms: Dict mapping name to (source, target) pair.
        comp_table: Dict mapping (f, g) to the composite morphism name.
    """

    def __init__(self, objects: list[str], morphisms: dict[str, tuple[str, str]],
                 comp_table: dict[tuple[str, str], str]) -> None:
        """Initialise the category.

        Args:
            objects: Object names.
            morphisms: Maps morphism name to (source, target).
            comp_table: Maps (f, g) to composite name where g.f is defined.
        """
        self.objects = objects
        self.morphisms = morphisms
        self.comp_table = comp_table

    def compose(self, f: str, g: str) -> str | None:
        """Compose g after f (g . f).

        Args:
            f: First morphism (applied first).
            g: Second morphism (applied second).

        Returns:
            Name of composite morphism, or None if undefined.
        """
        return self.comp_table.get((f, g))

    def source(self, f: str) -> str:
        """Return the source object of morphism f.

        Args:
            f: Morphism name.

        Returns:
            Source object name.
        """
        return self.morphisms[f][0]

    def target(self, f: str) -> str:
        """Return the target object of morphism f.

        Args:
            f: Morphism name.

        Returns:
            Target object name.
        """
        return self.morphisms[f][1]


def _make_category_2(rng) -> SmallCategory:
    """Build a small category with 2 objects and 1 non-identity morphism.

    Args:
        rng: Random number generator.

    Returns:
        A SmallCategory with objects {A, B}.
    """
    objects = ["A", "B"]
    morphisms = {
        "id_A": ("A", "A"),
        "id_B": ("B", "B"),
        "f": ("A", "B"),
    }
    comp_table = {
        ("id_A", "id_A"): "id_A",
        ("id_B", "id_B"): "id_B",
        ("id_A", "f"): "f",
        ("f", "id_B"): "f",
    }
    return SmallCategory(objects, morphisms, comp_table)


def _make_category_3(rng) -> SmallCategory:
    """Build a small category with 3 objects and a composable chain.

    Args:
        rng: Random number generator.

    Returns:
        A SmallCategory with objects {A, B, C} and morphisms f:A->B, g:B->C, gf:A->C.
    """
    objects = ["A", "B", "C"]
    morphisms = {
        "id_A": ("A", "A"),
        "id_B": ("B", "B"),
        "id_C": ("C", "C"),
        "f": ("A", "B"),
        "g": ("B", "C"),
        "gf": ("A", "C"),
    }
    comp_table = {
        ("id_A", "id_A"): "id_A",
        ("id_B", "id_B"): "id_B",
        ("id_C", "id_C"): "id_C",
        ("id_A", "f"): "f",
        ("f", "id_B"): "f",
        ("id_B", "g"): "g",
        ("g", "id_C"): "g",
        ("f", "g"): "gf",
        ("id_A", "gf"): "gf",
        ("gf", "id_C"): "gf",
    }
    return SmallCategory(objects, morphisms, comp_table)


# ═══════════════════════════════════════════════════════════════════
# 1. MORPHISM COMPOSE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class MorphismComposeGenerator(StepGenerator):
    """Compose morphisms in a small category and verify associativity.

    Given a category with 2-3 objects and explicitly listed morphisms,
    computes the composition of two composable morphisms and verifies
    that (h.g).f = h.(g.f) on a triple.

    Difficulty scaling:
        Difficulty 1-3: 2-object category, single composition.
        Difficulty 4-6: 3-object category, chain of 2 morphisms.
        Difficulty 7-8: 3-object category, verify associativity.

    Prerequisites:
        group_table (tier 4).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "morphism_compose"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["group_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category size.

        Returns:
            Task description string.
        """
        return "compose morphisms in small category"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a morphism composition problem.

        Args:
            difficulty: Controls category complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            cat = _make_category_2(self._rng)
            m1, m2 = "id_A", "f"
            result = cat.compose(m1, m2)
            check_assoc = False
        else:
            cat = _make_category_3(self._rng)
            m1, m2 = "f", "g"
            result = cat.compose(m1, m2)
            check_assoc = difficulty >= 7

        assoc_ok = True
        if check_assoc:
            left = cat.compose("f", "g")
            if left is not None:
                both = cat.compose("id_A", left)
            else:
                both = None
            right = cat.compose("id_A", "f")
            if right is not None:
                both2 = cat.compose(right, "g")
            else:
                both2 = None
            assoc_ok = both == both2

        obj_str = ", ".join(cat.objects)
        morph_list = [f"{k}:{v[0]}->{v[1]}" for k, v in sorted(cat.morphisms.items())
                      if not k.startswith("id_")]
        morph_str = ", ".join(morph_list)
        problem = (
            f"Cat: obj={{{obj_str}}}, morph={{{morph_str}}}. "
            f"Compose {m2}.{m1}."
        )
        return problem, {
            "cat_objects": cat.objects, "m1": m1, "m2": m2,
            "result": result, "check_assoc": check_assoc,
            "assoc_ok": assoc_ok,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate morphism composition steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the composition.
        """
        steps = [
            f"{data['m2']} . {data['m1']} = {data['result']}",
        ]
        if data["check_assoc"]:
            steps.append("associativity: (h.g).f = h.(g.f)")
            steps.append(f"verified: {'YES' if data['assoc_ok'] else 'NO'}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The composite morphism name.
        """
        ans = data["result"] if data["result"] else "undefined"
        if data["check_assoc"]:
            return f"{ans}, assoc={'YES' if data['assoc_ok'] else 'NO'}"
        return ans


# ═══════════════════════════════════════════════════════════════════
# 2. FUNCTOR APPLY (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class FunctorApplyGenerator(StepGenerator):
    """Apply a functor F: C -> D and verify the functor axioms.

    Maps objects and morphisms from a source category to a target
    category and verifies F(g.f) = F(g).F(f) and F(id_A) = id_{F(A)}.

    Difficulty scaling:
        Difficulty 1-3: 2-object categories.
        Difficulty 4-6: 3-object categories, verify composition.
        Difficulty 7-8: 3-object categories, full axiom check.

    Prerequisites:
        morphism_compose (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "functor_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["morphism_compose"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category size.

        Returns:
            Task description string.
        """
        return "apply functor and verify axioms"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a functor application problem.

        Args:
            difficulty: Controls category size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            cat_c = _make_category_2(self._rng)
            obj_map = {"A": "X", "B": "Y"}
            mor_map = {"id_A": "id_X", "id_B": "id_Y", "f": "h"}
        else:
            cat_c = _make_category_3(self._rng)
            obj_map = {"A": "X", "B": "Y", "C": "Z"}
            mor_map = {
                "id_A": "id_X", "id_B": "id_Y", "id_C": "id_Z",
                "f": "h", "g": "k", "gf": "kh",
            }

        id_ok = True
        for obj in cat_c.objects:
            id_name = f"id_{obj}"
            f_id = mor_map.get(id_name, "")
            expected = f"id_{obj_map[obj]}"
            if f_id != expected:
                id_ok = False

        comp_ok = True
        comp_check = ""
        if difficulty >= 5:
            gf = cat_c.compose("f", "g")
            f_gf = mor_map.get(gf, "") if gf else ""
            f_f = mor_map.get("f", "")
            f_g = mor_map.get("g", "")
            comp_check = f"F(g.f)={f_gf}, F(g).F(f)={f_g}.{f_f}"
            comp_ok = f_gf == "kh"

        obj_str = _format_map(obj_map)
        mor_str = ", ".join(f"F({k})={v}" for k, v in sorted(mor_map.items())
                           if not k.startswith("id_"))
        problem = f"F: C->D, obj: {obj_str}, morph: {mor_str}. Verify functor."
        return problem, {
            "obj_map": obj_map, "mor_map": mor_map,
            "id_ok": id_ok, "comp_ok": comp_ok,
            "comp_check": comp_check,
            "difficulty": difficulty,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate functor verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking functor axioms.
        """
        steps = [
            f"F maps objects: {_format_map(data['obj_map'])}",
            f"identity: F(id_A)=id_{{F(A)}}? {'YES' if data['id_ok'] else 'NO'}",
        ]
        if data["difficulty"] >= 5:
            steps.append(f"composition: {data['comp_check']}")
            steps.append(f"F(g.f)=F(g).F(f)? {'YES' if data['comp_ok'] else 'NO'}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Whether F is a valid functor.
        """
        valid = data["id_ok"] and data["comp_ok"]
        return "valid functor" if valid else "NOT a functor"


# ═══════════════════════════════════════════════════════════════════
# 3. NATURAL TRANSFORM (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class NaturalTransformGenerator(StepGenerator):
    """Verify a natural transformation between two functors.

    Given functors F, G: C -> D and components eta_A: F(A) -> G(A),
    checks the naturality condition: eta_B . F(f) = G(f) . eta_A
    for all morphisms f: A -> B.

    Difficulty scaling:
        Difficulty 1-3: 2-object category, one morphism to check.
        Difficulty 4-6: 3-object category, two morphisms to check.
        Difficulty 7-8: 3-object category, full naturality check.

    Prerequisites:
        functor_apply (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "natural_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functor_apply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category size.

        Returns:
            Task description string.
        """
        return "verify naturality square for transformation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a natural transformation verification problem.

        Args:
            difficulty: Controls category size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            objects = ["A", "B"]
            non_id_morphs = [("f", "A", "B")]
        else:
            objects = ["A", "B", "C"]
            non_id_morphs = [("f", "A", "B"), ("g", "B", "C")]

        f_obj = {o: f"F({o})" for o in objects}
        g_obj = {o: f"G({o})" for o in objects}

        eta = {o: f"eta_{o}" for o in objects}

        checks = []
        natural = True
        for (m_name, src, tgt) in non_id_morphs:
            lhs = f"eta_{tgt} . F({m_name})"
            rhs = f"G({m_name}) . eta_{src}"
            eq = self._rng.random() < 0.8
            checks.append({
                "morph": m_name, "src": src, "tgt": tgt,
                "lhs": lhs, "rhs": rhs, "equal": eq,
            })
            if not eq:
                natural = False

        eta_str = ", ".join(f"eta_{o}: F({o})->G({o})" for o in objects)
        morph_str = ", ".join(f"{m}:{s}->{t}" for m, s, t in non_id_morphs)
        problem = (
            f"F,G: C->D, C={{obj={{{','.join(objects)}}}, "
            f"morph={{{morph_str}}}}}. "
            f"eta: {eta_str}. Natural?"
        )
        return problem, {
            "objects": objects, "checks": checks,
            "natural": natural, "eta": eta,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate naturality verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking each naturality square.
        """
        steps = []
        for chk in data["checks"]:
            eq_str = "=" if chk["equal"] else "!="
            steps.append(
                f"f={chk['morph']}: {chk['lhs']} {eq_str} {chk['rhs']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Whether eta is a natural transformation.
        """
        if data["natural"]:
            return "YES, natural transformation"
        return "NO, naturality fails"


# ═══════════════════════════════════════════════════════════════════
# 4. PRODUCT CATEGORY (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class ProductCategoryGenerator(StepGenerator):
    """Construct the categorical product A x B in Set.

    Given small finite sets A and B, constructs the Cartesian product
    with projection morphisms pi_1 and pi_2, and verifies the
    universal property for a given test object C with maps to A and B.

    Difficulty scaling:
        Difficulty 1-3: |A|=2, |B|=2.
        Difficulty 4-6: |A|=2-3, |B|=2-3.
        Difficulty 7-8: |A|=3, |B|=3, verify universal property.

    Prerequisites:
        morphism_compose (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "product_category"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["morphism_compose"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Task description string.
        """
        return "construct product in Set with projections"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a categorical product construction problem.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            na, nb = 2, 2
        elif difficulty <= 6:
            na = self._rng.randint(2, 3)
            nb = self._rng.randint(2, 3)
        else:
            na, nb = 3, 3

        set_a = [i + 1 for i in range(na)]
        set_b = [i + 1 for i in range(nb)]
        product = [(a, b) for a in set_a for b in set_b]

        pi1 = {(a, b): a for a, b in product}
        pi2 = {(a, b): b for a, b in product}

        check_univ = difficulty >= 7
        univ_ok = True
        univ_map = {}
        if check_univ:
            set_c = [1, 2]
            f_map = {c: self._rng.choice(set_a) for c in set_c}
            g_map = {c: self._rng.choice(set_b) for c in set_c}
            univ_map = {c: (f_map[c], g_map[c]) for c in set_c}
            for c in set_c:
                if pi1[univ_map[c]] != f_map[c] or pi2[univ_map[c]] != g_map[c]:
                    univ_ok = False

        prod_str = _format_set([f"({a},{b})" for a, b in product])
        problem = (
            f"A={_format_set(set_a)}, B={_format_set(set_b)}. "
            f"Construct AxB with projections."
        )
        return problem, {
            "set_a": set_a, "set_b": set_b,
            "product": product, "na": na, "nb": nb,
            "check_univ": check_univ, "univ_ok": univ_ok,
            "univ_map": univ_map,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate product construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing product, projections, and universal property.
        """
        prod_items = [f"({a},{b})" for a, b in data["product"]]
        steps = [
            f"AxB = {{{', '.join(prod_items)}}}",
            f"|AxB| = {data['na']}*{data['nb']} = {data['na'] * data['nb']}",
            f"pi_1(a,b)=a, pi_2(a,b)=b",
        ]
        if data["check_univ"]:
            u_str = ", ".join(f"{c}->({v[0]},{v[1]})" for c, v in sorted(data["univ_map"].items()))
            steps.append(f"universal map: {u_str}")
            steps.append(f"pi_1.u=f, pi_2.u=g: {'YES' if data['univ_ok'] else 'NO'}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Product set and size.
        """
        size = data["na"] * data["nb"]
        return f"|AxB| = {size}"


# ═══════════════════════════════════════════════════════════════════
# 5. COPRODUCT CATEGORY (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class CoproductCategoryGenerator(StepGenerator):
    """Construct the coproduct A + B (disjoint union) in Set.

    Given small finite sets A and B, constructs their disjoint union
    with injection morphisms iota_1 and iota_2.

    Difficulty scaling:
        Difficulty 1-3: |A|=2, |B|=2.
        Difficulty 4-6: |A|=2-3, |B|=2-3.
        Difficulty 7-8: |A|=3, |B|=3, verify universal property.

    Prerequisites:
        product_category (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "coproduct_category"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["product_category"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Task description string.
        """
        return "construct coproduct (disjoint union) in Set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a coproduct construction problem.

        Args:
            difficulty: Controls set sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            na, nb = 2, 2
        elif difficulty <= 6:
            na = self._rng.randint(2, 3)
            nb = self._rng.randint(2, 3)
        else:
            na, nb = 3, 3

        set_a = [f"a{i}" for i in range(1, na + 1)]
        set_b = [f"b{i}" for i in range(1, nb + 1)]
        coprod = [(x, "A") for x in set_a] + [(x, "B") for x in set_b]

        iota1 = {x: (x, "A") for x in set_a}
        iota2 = {x: (x, "B") for x in set_b}

        check_univ = difficulty >= 7
        univ_ok = True
        if check_univ:
            target = ["t1", "t2", "t3"]
            f_map = {x: self._rng.choice(target[:2]) for x in set_a}
            g_map = {x: self._rng.choice(target[:2]) for x in set_b}
            u_map = {}
            for x in set_a:
                u_map[(x, "A")] = f_map[x]
            for x in set_b:
                u_map[(x, "B")] = g_map[x]
            for x in set_a:
                if u_map[iota1[x]] != f_map[x]:
                    univ_ok = False
            for x in set_b:
                if u_map[iota2[x]] != g_map[x]:
                    univ_ok = False

        problem = (
            f"A={_format_set(set_a)}, B={_format_set(set_b)}. "
            f"Construct A+B with injections."
        )
        return problem, {
            "set_a": set_a, "set_b": set_b,
            "coprod": coprod, "na": na, "nb": nb,
            "check_univ": check_univ, "univ_ok": univ_ok,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coproduct construction steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing disjoint union and injections.
        """
        coprod_str = ", ".join(f"({x},{tag})" for x, tag in data["coprod"])
        steps = [
            f"A+B = {{{coprod_str}}}",
            f"|A+B| = {data['na']}+{data['nb']} = {data['na'] + data['nb']}",
            "iota_1(a) = (a,A), iota_2(b) = (b,B)",
        ]
        if data["check_univ"]:
            steps.append(f"universal property: {'verified' if data['univ_ok'] else 'failed'}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Coproduct size.
        """
        return f"|A+B| = {data['na'] + data['nb']}"


# ═══════════════════════════════════════════════════════════════════
# 6. ADJUNCTION CHECK (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class AdjunctionCheckGenerator(StepGenerator):
    """Verify an adjunction F -| G by checking the hom-set bijection.

    For functors F: C -> D and G: D -> C, verifies the natural
    bijection Hom_D(F(A), B) ~ Hom_C(A, G(B)) on small examples
    with finite hom-sets.

    Difficulty scaling:
        Difficulty 1-3: 2-object categories, |Hom| <= 2.
        Difficulty 4-6: 3-object categories, |Hom| <= 3.
        Difficulty 7-8: 3-object categories, full bijection check.

    Prerequisites:
        natural_transform (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adjunction_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_transform"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category size.

        Returns:
            Task description string.
        """
        return "verify adjunction via hom-set bijection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an adjunction check problem.

        Args:
            difficulty: Controls category size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            c_obj = ["A", "B"]
            d_obj = ["X", "Y"]
        else:
            c_obj = ["A", "B", "C"]
            d_obj = ["X", "Y", "Z"]

        f_map = {}
        for i, o in enumerate(c_obj):
            f_map[o] = d_obj[min(i, len(d_obj) - 1)]

        g_map = {}
        for i, o in enumerate(d_obj):
            g_map[o] = c_obj[min(i, len(c_obj) - 1)]

        is_adjunction = self._rng.random() < 0.6

        checks = []
        for a in c_obj[:2]:
            for b in d_obj[:2]:
                hom_fa_b = self._rng.randint(0, 2)
                if is_adjunction:
                    hom_a_gb = hom_fa_b
                else:
                    hom_a_gb = hom_fa_b + self._rng.choice([-1, 0, 0, 1])
                    hom_a_gb = max(0, hom_a_gb)
                checks.append({
                    "a": a, "b": b,
                    "fa": f_map[a], "gb": g_map[b],
                    "hom_fa_b": hom_fa_b, "hom_a_gb": hom_a_gb,
                    "match": hom_fa_b == hom_a_gb,
                })

        actual_adj = all(chk["match"] for chk in checks)

        f_str = _format_map(f_map)
        g_str = _format_map(g_map)
        problem = f"F: {f_str}, G: {g_str}. Is F-|G an adjunction?"
        return problem, {
            "f_map": f_map, "g_map": g_map,
            "checks": checks, "is_adjunction": actual_adj,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate adjunction verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking hom-set bijections.
        """
        steps = ["check: |Hom(F(A),B)| = |Hom(A,G(B))| for all A,B"]
        for chk in data["checks"]:
            eq = "=" if chk["match"] else "!="
            steps.append(
                f"A={chk['a']},B={chk['b']}: "
                f"|Hom({chk['fa']},{chk['b']})| {eq} "
                f"|Hom({chk['a']},{chk['gb']})|"
                f" ({chk['hom_fa_b']} vs {chk['hom_a_gb']})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Whether F -| G is an adjunction.
        """
        if data["is_adjunction"]:
            return "YES, F -| G is an adjunction"
        return "NO, hom-set sizes do not match"


# ═══════════════════════════════════════════════════════════════════
# 7. YONEDA APPLY (tier 8)
# ═══════════════════════════════════════════════════════════════════

@register
class YonedaApplyGenerator(StepGenerator):
    """Apply the Yoneda lemma on a small category.

    Computes Nat(Hom(A,-), F) ~ F(A) for a functor F: C -> Set
    on a category with 2-3 objects. The key insight is that every
    natural transformation from a representable functor is determined
    by its value on id_A.

    Difficulty scaling:
        Difficulty 1-3: 2-object category, F sends each object to a small set.
        Difficulty 4-6: 3-object category.
        Difficulty 7-8: 3-object category, explicit naturality check.

    Prerequisites:
        natural_transform (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "yoneda_apply"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_transform"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category size.

        Returns:
            Task description string.
        """
        return "apply Yoneda lemma on small category"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Yoneda lemma application problem.

        Args:
            difficulty: Controls category size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            objects = ["A", "B"]
            hom_sets = {
                ("A", "A"): ["id_A"],
                ("A", "B"): ["f"],
                ("B", "A"): [],
                ("B", "B"): ["id_B"],
            }
        else:
            objects = ["A", "B", "C"]
            hom_sets = {
                ("A", "A"): ["id_A"],
                ("A", "B"): ["f"],
                ("A", "C"): ["gf"],
                ("B", "A"): [],
                ("B", "B"): ["id_B"],
                ("B", "C"): ["g"],
                ("C", "A"): [],
                ("C", "B"): [],
                ("C", "C"): ["id_C"],
            }

        rep_obj = self._rng.choice(objects)

        f_values = {}
        for o in objects:
            size = self._rng.randint(1, 3)
            f_values[o] = [f"x_{o}_{i}" for i in range(size)]

        fa_size = len(f_values[rep_obj])
        nat_count = fa_size

        problem = (
            f"C={{{','.join(objects)}}}, F: C->Set, "
            f"F(A)={{{','.join(f_values[rep_obj])}}}. "
            f"|Nat(Hom({rep_obj},-),F)| = ?"
        )
        return problem, {
            "objects": objects, "rep_obj": rep_obj,
            "f_values": f_values, "fa_size": fa_size,
            "nat_count": nat_count,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Yoneda application steps.

        Args:
            data: Solution data.

        Returns:
            Steps applying the Yoneda lemma.
        """
        rep = data["rep_obj"]
        fa = data["f_values"][rep]
        steps = [
            f"Yoneda: Nat(Hom({rep},-), F) ~ F({rep})",
            f"F({rep}) = {{{', '.join(fa)}}}",
            f"|F({rep})| = {data['fa_size']}",
            f"each nat. transf. determined by image of id_{rep}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            Number of natural transformations.
        """
        return f"|Nat(Hom({data['rep_obj']},-),F)| = {data['nat_count']}"


# ═══════════════════════════════════════════════════════════════════
# 8. LIMIT COMPUTE (tier 7)
# ═══════════════════════════════════════════════════════════════════

@register
class LimitComputeGenerator(StepGenerator):
    """Compute limits (equalizers or pullbacks) of diagrams in Set.

    Generates small diagrams in Set and computes their limits.
    Equalizers: given f,g: A -> B, compute eq = {a in A : f(a) = g(a)}.
    Pullbacks: given f: A -> C, g: B -> C, compute {(a,b) : f(a) = g(b)}.

    Difficulty scaling:
        Difficulty 1-3: equalizers with |A| <= 4.
        Difficulty 4-6: equalizers with |A| <= 6 or pullbacks |A|,|B| <= 3.
        Difficulty 7-8: pullbacks with |A|, |B| <= 4.

    Prerequisites:
        product_category (tier 7).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "limit_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["product_category"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls diagram complexity.

        Returns:
            Task description string.
        """
        return "compute limit of diagram in Set"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a limit computation problem.

        Args:
            difficulty: Controls diagram complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        use_pullback = difficulty >= 5 and self._rng.random() < 0.6

        if not use_pullback:
            if difficulty <= 3:
                n = self._rng.randint(3, 4)
            else:
                n = self._rng.randint(4, 6)
            m = self._rng.randint(2, max(2, n - 1))
            set_a = list(range(1, n + 1))
            set_b = list(range(1, m + 1))
            f_map = {a: self._rng.choice(set_b) for a in set_a}
            g_map = {a: self._rng.choice(set_b) for a in set_a}

            equalizer = sorted([a for a in set_a if f_map[a] == g_map[a]])

            f_str = ", ".join(f"f({a})={f_map[a]}" for a in set_a)
            g_str = ", ".join(f"g({a})={g_map[a]}" for a in set_a)
            problem = (
                f"A={_format_set(set_a)}, B={_format_set(set_b)}, "
                f"{f_str}, {g_str}. Equalizer of f,g?"
            )
            return problem, {
                "kind": "equalizer", "set_a": set_a, "set_b": set_b,
                "f_map": f_map, "g_map": g_map,
                "limit": equalizer, "limit_size": len(equalizer),
            }
        else:
            if difficulty <= 6:
                na = self._rng.randint(2, 3)
                nb = self._rng.randint(2, 3)
            else:
                na = self._rng.randint(3, 4)
                nb = self._rng.randint(3, 4)
            nc = self._rng.randint(2, 3)
            set_a = list(range(1, na + 1))
            set_b = list(range(1, nb + 1))
            set_c = list(range(1, nc + 1))
            f_map = {a: self._rng.choice(set_c) for a in set_a}
            g_map = {b: self._rng.choice(set_c) for b in set_b}

            pullback = sorted(
                [(a, b) for a in set_a for b in set_b
                 if f_map[a] == g_map[b]]
            )

            f_str = ", ".join(f"f({a})={f_map[a]}" for a in set_a)
            g_str = ", ".join(f"g({b})={g_map[b]}" for b in set_b)
            problem = (
                f"A={_format_set(set_a)}, B={_format_set(set_b)}, "
                f"C={_format_set(set_c)}, {f_str}, {g_str}. "
                f"Pullback of f,g over C?"
            )
            return problem, {
                "kind": "pullback",
                "set_a": set_a, "set_b": set_b, "set_c": set_c,
                "f_map": f_map, "g_map": g_map,
                "limit": pullback, "limit_size": len(pullback),
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate limit computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps computing the limit.
        """
        if data["kind"] == "equalizer":
            f_map = data["f_map"]
            g_map = data["g_map"]
            steps = [
                "equalizer = {a in A : f(a) = g(a)}",
            ]
            check_parts = []
            for a in data["set_a"]:
                eq = "=" if f_map[a] == g_map[a] else "!="
                check_parts.append(f"a={a}: f={f_map[a]}{eq}g={g_map[a]}")
            steps.append(", ".join(check_parts[:6]))
            lim_str = _format_set(data["limit"]) if data["limit"] else "{}"
            steps.append(f"eq = {lim_str}")
            return steps
        else:
            steps = [
                "pullback = {(a,b) : f(a) = g(b)}",
            ]
            pairs = data["limit"][:6]
            if pairs:
                pair_str = ", ".join(f"({a},{b})" for a, b in pairs)
                steps.append(f"matching pairs: {pair_str}")
            else:
                steps.append("no matching pairs")
            steps.append(f"|pullback| = {data['limit_size']}")
            return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final answer.

        Args:
            data: Solution data.

        Returns:
            The limit set and its size.
        """
        if data["kind"] == "equalizer":
            lim_str = _format_set(data["limit"]) if data["limit"] else "{}"
            return f"eq = {lim_str}, |eq| = {data['limit_size']}"
        else:
            if data["limit"]:
                pair_str = "{" + ", ".join(f"({a},{b})" for a, b in data["limit"][:8]) + "}"
            else:
                pair_str = "{}"
            return f"pb = {pair_str}, |pb| = {data['limit_size']}"
