"""Extended category theory generators for tiers 7-8.

6 generators covering monad computation, Kan extensions, enriched
categories, topos basics, adjunction unit/counit, and abelian
categories. All use small finite category examples to stay under
512 characters.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# -- Formatting helpers -----------------------------------------------


def _format_set(elements: list | set) -> str:
    """Format a collection as a set string.

    Args:
        elements: Iterable of elements to format.

    Returns:
        String like ``{A, B, C}``.
    """
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


# =====================================================================
# 1. MONAD COMPUTE (tier 7)
# =====================================================================

@register
class MonadComputeGenerator(StepGenerator):
    """Apply a monad (T, eta, mu) to concrete data.

    For the List monad: T(X) = List(X), eta(x) = [x], mu = flatten.
    For the Maybe monad: T(X) = X + {Nothing}, eta(x) = Just(x).
    Apply to nested structures and verify monad laws.

    Difficulty scaling:
        Difficulty 1-3: List monad, eta and mu on simple lists.
        Difficulty 4-6: List monad, verify unit/associativity laws.
        Difficulty 7-8: Maybe monad, Kleisli composition.

    Prerequisites:
        functor_apply (tier 7).
    """

    _LIST_EASY = [
        ([1, 2, 3], [[1, 2, 3]],
         "eta([1,2,3]) = [[1,2,3]]"),
        ([[1, 2], [3]], [1, 2, 3],
         "mu([[1,2],[3]]) = flatten = [1,2,3]"),
        ([5], [[5]],
         "eta([5]) = [[5]]"),
    ]

    _LIST_MED = [
        ([[[1], [2]], [[3]]], [[1], [2], [3]],
         "mu([[[1],[2]],[[3]]]) = [[1],[2],[3]]"),
        ([[1]], [1],
         "mu([[1]]) = [1], also mu(eta([1])) = [1] (left unit)"),
        ([[1, 2], [3, 4], [5]], [1, 2, 3, 4, 5],
         "mu flattens one level"),
    ]

    _MAYBE_HARD = [
        ("Just(3)", "Just(Just(3))",
         "eta(Just(3)) = Just(Just(3))"),
        ("Just(Just(5))", "Just(5)",
         "mu(Just(Just(5))) = Just(5)"),
        ("Nothing", "Nothing",
         "mu(Nothing) = Nothing"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "monad_compute"

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
            difficulty: Controls monad type.

        Returns:
            Task description string.
        """
        return "apply monad operations (eta, mu) to data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a monad computation problem.

        Args:
            difficulty: Controls monad type and operation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._LIST_EASY
            inp, out, reason = self._rng.choice(pool)
            op = "eta" if isinstance(out, list) and isinstance(out[0], list) and not isinstance(inp[0], list) else "mu"
            problem = (
                f"List monad. {op}({inp}). Compute."
            )
            return problem, {
                "monad": "List", "op": op, "input": str(inp),
                "output": str(out), "reason": reason,
            }
        elif difficulty <= 6:
            pool = self._LIST_MED
            inp, out, reason = self._rng.choice(pool)
            problem = f"List monad. mu({inp}). Compute."
            return problem, {
                "monad": "List", "op": "mu", "input": str(inp),
                "output": str(out), "reason": reason,
            }
        else:
            pool = self._MAYBE_HARD
            inp, out, reason = self._rng.choice(pool)
            op = "mu" if "mu" in reason.lower() else "eta"
            problem = f"Maybe monad. {op}({inp}). Compute."
            return problem, {
                "monad": "Maybe", "op": op, "input": inp,
                "output": out, "reason": reason,
            }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate monad operation steps.

        Args:
            data: Solution data.

        Returns:
            Steps showing the monad operation.
        """
        return [
            f"monad: {data['monad']}",
            f"{data['op']}({data['input']})",
            data["reason"],
            f"result: {data['output']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the result of the monad operation.

        Args:
            data: Solution data.

        Returns:
            Result value.
        """
        return f"{data['op']}({data['input']}) = {data['output']}"


# =====================================================================
# 2. KAN EXTENSION (tier 8)
# =====================================================================

@register
class KanExtensionGenerator(StepGenerator):
    """Compute left Kan extension of a functor along another.

    Lan_F(G)(c) = colim_{(F(a)->c)} G(a). For finite categories,
    the colimit reduces to a coproduct over the comma category.
    Template-based for small categories with 2-3 objects.

    Difficulty scaling:
        Difficulty 1-3: both categories have 2 objects, F is inclusion.
        Difficulty 4-6: 3-object source, 2-object target.
        Difficulty 7-8: 3-object categories, compute actual colimits.

    Prerequisites:
        functor_apply (tier 7).
    """

    _EXTENSIONS_EASY = [
        ("F: {A} -> {A,B} (inclusion), G: {A} -> Set, G(A) = {1,2}",
         "Lan_F(G)(A) = {1,2}", "Lan_F(G)(B) = {} (initial)",
         "left Kan extends by taking colimit over empty comma category for B"),
        ("F: {A} -> {A,B} (inclusion), G: {A} -> Set, G(A) = {x}",
         "Lan_F(G)(A) = {x}", "Lan_F(G)(B) = {}",
         "singleton extended, B gets initial object"),
    ]

    _EXTENSIONS_MED = [
        ("F: {A,B} -> {X} (collapse), G(A)={1,2}, G(B)={3}",
         "Lan_F(G)(X) = {1,2,3}", "",
         "colimit over A,B mapping to X = coproduct G(A)+G(B)"),
        ("F: {A,B} -> {X,Y}, F(A)=X, F(B)=Y, G(A)={a}, G(B)={b,c}",
         "Lan_F(G)(X) = {a}", "Lan_F(G)(Y) = {b,c}",
         "F is bijection on objects, Lan = G.F^{-1}"),
    ]

    _EXTENSIONS_HARD = [
        ("F: {A,B,C} -> {X,Y}, F(A)=F(C)=X, F(B)=Y, G(A)={1}, G(B)={2}, G(C)={3}",
         "Lan_F(G)(X) = {1,3}", "Lan_F(G)(Y) = {2}",
         "colimit at X over A,C = coproduct {1}+{3}"),
        ("F: {A} -> {X,Y,Z}, F(A)=Y, G(A)={a,b}",
         "Lan_F(G)(Y) = {a,b}", "Lan_F(G)(X) = Lan_F(G)(Z) = {}",
         "only Y has objects in comma category"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kan_extension"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functor_apply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls category sizes.

        Returns:
            Task description string.
        """
        return "compute left Kan extension on finite categories"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kan extension problem.

        Args:
            difficulty: Controls category complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._EXTENSIONS_EASY
        elif difficulty <= 6:
            pool = self._EXTENSIONS_EASY + self._EXTENSIONS_MED
        else:
            pool = self._EXTENSIONS_EASY + self._EXTENSIONS_MED + self._EXTENSIONS_HARD

        desc, result1, result2, reason = self._rng.choice(pool)
        problem = f"{desc}. Compute Lan_F(G)."
        return problem, {
            "desc": desc, "result1": result1,
            "result2": result2, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kan extension computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the colimit computation.
        """
        steps = [
            "Lan_F(G)(c) = colim_{(F(a)->c)} G(a)",
            f"setup: {data['desc']}",
            data["reason"],
            data["result1"],
        ]
        if data["result2"]:
            steps.append(data["result2"])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Kan extension values.

        Args:
            data: Solution data.

        Returns:
            Kan extension at each object.
        """
        if data["result2"]:
            return f"{data['result1']}; {data['result2']}"
        return data["result1"]


# =====================================================================
# 3. ENRICHED CATEGORY (tier 7)
# =====================================================================

@register
class EnrichedCategoryGenerator(StepGenerator):
    """Identify enriched categories from the enriching category V.

    A category enriched over (V, tensor, I) has Hom-objects in V.
    For V = Bool (truth values): preorder. For V = Set: ordinary
    category. For V = Ab: preadditive category. Template-based.

    Difficulty scaling:
        Difficulty 1-3: V = Bool, identify as preorder.
        Difficulty 4-6: V = Set, ordinary category examples.
        Difficulty 7-8: V = Ab or V = Vect, preadditive structure.

    Prerequisites:
        morphism_compose (tier 7).
    """

    _ENRICHMENTS_EASY = [
        ("V = Bool = ({false, true}, AND, true)",
         "preorder",
         "Hom(A,B) = true/false, composition = AND, reflexivity = true",
         "example: (Z, <=) is Bool-enriched"),
        ("V = Bool, objects = {1,2,3}, Hom(i,j) = (i <= j)",
         "preorder on {1,2,3}",
         "1<=2<=3, transitivity = AND of Hom values",
         "finite totally ordered set"),
    ]

    _ENRICHMENTS_MED = [
        ("V = Set = (Set, x, {*})",
         "ordinary (locally small) category",
         "Hom(A,B) is a set, composition is a function",
         "example: category of groups, vector spaces"),
        ("V = Set, objects = {A,B}, Hom(A,B) = {f,g}, Hom(B,A) = {h}",
         "finite category with 2 objects",
         "|Hom(A,B)| = 2, |Hom(B,A)| = 1",
         "ordinary category with multiple morphisms"),
    ]

    _ENRICHMENTS_HARD = [
        ("V = Ab = (abelian groups, tensor, Z)",
         "preadditive category",
         "Hom(A,B) is abelian group, composition is bilinear",
         "example: category of R-modules"),
        ("V = Vect_k = (k-vector spaces, tensor, k)",
         "k-linear category",
         "Hom(A,B) is k-vector space, composition is k-bilinear",
         "example: category of f.d. representations"),
        ("V = [0,inf] = (extended reals, +, 0)",
         "generalised metric space (Lawvere)",
         "Hom(A,B) = d(A,B) >= 0, triangle inequality = composition",
         "enrichment captures metric space axioms"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "enriched_category"

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
            difficulty: Controls enrichment type.

        Returns:
            Task description string.
        """
        return "identify enriched category from enriching category V"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an enriched category identification problem.

        Args:
            difficulty: Controls enrichment type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._ENRICHMENTS_EASY
        elif difficulty <= 6:
            pool = self._ENRICHMENTS_EASY + self._ENRICHMENTS_MED
        else:
            pool = self._ENRICHMENTS_EASY + self._ENRICHMENTS_MED + self._ENRICHMENTS_HARD

        desc, cat_type, structure, example = self._rng.choice(pool)
        problem = f"{desc}. What kind of category is this?"
        return problem, {
            "desc": desc, "cat_type": cat_type,
            "structure": structure, "example": example,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate enriched category identification steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the enrichment.
        """
        return [
            f"enriching category: {data['desc']}",
            data["structure"],
            data["example"],
            f"V-enriched category = {data['cat_type']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the category type.

        Args:
            data: Solution data.

        Returns:
            Enriched category type.
        """
        return data["cat_type"]


# =====================================================================
# 4. TOPOS BASICS (tier 8)
# =====================================================================

@register
class ToposBasicsGenerator(StepGenerator):
    """Apply subobject classifier in elementary topoi.

    In Set: Omega = {true, false}, chi_A(x) = true iff x in A.
    The subobject classifier is the characteristic function of a
    subobject. Template-based for Set and presheaf topoi.

    Difficulty scaling:
        Difficulty 1-3: Set topos, compute chi_A for small sets.
        Difficulty 4-6: verify that chi classifies subobjects.
        Difficulty 7-8: presheaf topos examples.

    Prerequisites:
        natural_transform (tier 7).
    """

    _PROBLEMS_EASY = [
        ("Set, X={1,2,3}, A={1,3}",
         "chi_A(1)=true, chi_A(2)=false, chi_A(3)=true",
         "Omega={true,false}, chi_A: X -> Omega classifies A",
         "standard subobject classifier in Set"),
        ("Set, X={a,b,c,d}, A={a,b}",
         "chi_A(a)=true, chi_A(b)=true, chi_A(c)=false, chi_A(d)=false",
         "characteristic function of subset",
         "chi_A^{-1}(true) = A"),
    ]

    _PROBLEMS_MED = [
        ("Set, X={1,2,3,4}, A=empty",
         "chi_A(x) = false for all x",
         "empty subobject classified by constant false map",
         "chi_{empty} = false: X -> Omega"),
        ("Set, X={1,2}, A=X",
         "chi_X(x) = true for all x",
         "full subobject classified by constant true map",
         "chi_X = true: X -> Omega"),
        ("verify pullback: A = chi_A^{-1}(true)",
         "A = {x in X : chi_A(x) = true}",
         "subobject is pullback of true: 1 -> Omega along chi_A",
         "universal property of subobject classifier"),
    ]

    _PROBLEMS_HARD = [
        ("presheaf Set^{C^op}, C = {* -> *}",
         "Omega(0) = {empty, {*}}, Omega(1) = {empty, {*}}",
         "sieves on each object form the subobject classifier",
         "Omega assigns to each object the set of sieves"),
        ("Set, power object P(X) = Omega^X",
         "|P(X)| = 2^|X|, elements are characteristic functions",
         "power object internalises Hom(-, Omega)",
         "in Set: P(X) = powerset of X"),
        ("Set, internal logic: Omega has Heyting algebra structure",
         "AND, OR, implies, not defined on {true, false}",
         "in Set, Omega is Boolean (classical logic)",
         "topos internal logic is intuitionistic in general"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "topos_basics"

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
            difficulty: Controls topos example complexity.

        Returns:
            Task description string.
        """
        return "apply subobject classifier in elementary topos"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a topos basics problem.

        Args:
            difficulty: Controls example complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._PROBLEMS_EASY
        elif difficulty <= 6:
            pool = self._PROBLEMS_EASY + self._PROBLEMS_MED
        else:
            pool = self._PROBLEMS_EASY + self._PROBLEMS_MED + self._PROBLEMS_HARD

        desc, result, explanation, context = self._rng.choice(pool)
        problem = f"{desc}. Compute/identify the subobject classifier."
        return problem, {
            "desc": desc, "result": result,
            "explanation": explanation, "context": context,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate topos computation steps.

        Args:
            data: Solution data.

        Returns:
            Steps explaining the subobject classifier.
        """
        return [
            f"setting: {data['desc']}",
            data["context"],
            data["explanation"],
            data["result"],
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the subobject classifier result.

        Args:
            data: Solution data.

        Returns:
            Result of the computation.
        """
        return data["result"]


# =====================================================================
# 5. ADJUNCTION UNIT COUNIT (tier 7)
# =====================================================================

@register
class AdjunctionUnitCounitGenerator(StepGenerator):
    """Verify triangle identities for an adjunction (F -| G).

    Given eta: Id -> GF (unit) and epsilon: FG -> Id (counit), verifies
    (epsilon*F) . (F*eta) = id_F and (G*epsilon) . (eta*G) = id_G
    on small examples.

    Difficulty scaling:
        Difficulty 1-3: free-forgetful adjunction on finite sets.
        Difficulty 4-6: concrete adjunction, verify one triangle identity.
        Difficulty 7-8: verify both triangle identities.

    Prerequisites:
        natural_transform (tier 7).
    """

    _ADJUNCTIONS_EASY = [
        ("F=Free: Set->Grp, G=Forgetful: Grp->Set",
         "eta(x) = x (as generator)", "epsilon(w) = evaluate word",
         True,
         "free-forgetful: eta includes set as generators"),
        ("F=(-)*2: Set->Set, G=(-)/2: Set->Set (on even sets)",
         "eta(x) = (x,x)", "epsilon((x,y)) = x",
         True,
         "diagonal-projection adjunction on finite sets"),
    ]

    _ADJUNCTIONS_MED = [
        ("F=Free: Set->Ab, G=Forget: Ab->Set",
         "eta(x) = x in Z^S", "epsilon: Z^{|G(A)|} -> A (evaluation)",
         True,
         "free abelian group adjunction"),
        ("F: Set->Set, F(X) = X + 1, G: Set->Set, G(Y) = Y",
         "eta(x) = inl(x)", "epsilon: Y+1 -> Y (retract)",
         False,
         "not an adjunction: triangle identity fails for G"),
    ]

    _ADJUNCTIONS_HARD = [
        ("F=Sigma_f: Set/A -> Set/B, G=f*: Set/B -> Set/A (pullback)",
         "eta: id -> f*.Sigma_f (unit of base change)",
         "epsilon: Sigma_f.f* -> id (counit)",
         True,
         "base change adjunction in slice categories"),
        ("tensor-hom: F=(-) tensor M, G=Hom(M,-) on Ab",
         "eta: A -> Hom(M, A tensor M)",
         "epsilon: Hom(M,B) tensor M -> B (evaluation)",
         True,
         "tensor-hom adjunction, both triangles hold"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adjunction_unit_counit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["natural_transform"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Controls adjunction complexity.

        Returns:
            Task description string.
        """
        return "verify triangle identities for adjunction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an adjunction unit/counit problem.

        Args:
            difficulty: Controls adjunction type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._ADJUNCTIONS_EASY
        elif difficulty <= 6:
            pool = self._ADJUNCTIONS_EASY + self._ADJUNCTIONS_MED
        else:
            pool = self._ADJUNCTIONS_EASY + self._ADJUNCTIONS_MED + self._ADJUNCTIONS_HARD

        desc, eta, epsilon, valid, reason = self._rng.choice(pool)
        problem = (
            f"{desc}. Unit: {eta}. Counit: {epsilon}. "
            f"Verify triangle identities."
        )
        return problem, {
            "desc": desc, "eta": eta, "epsilon": epsilon,
            "valid": valid, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate triangle identity verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking the identities.
        """
        valid_str = "YES" if data["valid"] else "NO"
        return [
            f"{data['desc'][:50]}",
            f"triangle 1: (eps*F).(F*eta)=id_F",
            f"triangle 2: (G*eps).(eta*G)=id_G",
            f"valid: {valid_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the adjunction validity.

        Args:
            data: Solution data.

        Returns:
            Whether the triangle identities hold.
        """
        if data["valid"]:
            return "valid adjunction (both triangle identities hold)"
        return "NOT a valid adjunction"


# =====================================================================
# 6. ABELIAN CATEGORY (tier 7)
# =====================================================================

@register
class AbelianCategoryGenerator(StepGenerator):
    """Verify exact sequences in abelian categories.

    In Ab (abelian groups), every morphism has a kernel and cokernel.
    Verifies exact sequences 0 -> A -> B -> C -> 0 by checking
    ker(g) = im(f) at each position.

    Difficulty scaling:
        Difficulty 1-3: short exact sequence of Z-modules.
        Difficulty 4-6: split exact sequences.
        Difficulty 7-8: non-split sequences, compute kernel/cokernel.

    Prerequisites:
        morphism_compose (tier 7).
    """

    _SEQUENCES_EASY = [
        ("0 -> Z --(x2)--> Z --(mod2)--> Z/2Z -> 0",
         True,
         "ker(mod2) = 2Z = im(x2), exact at Z",
         "multiplication by 2 followed by mod 2"),
        ("0 -> Z --(x3)--> Z --(mod3)--> Z/3Z -> 0",
         True,
         "ker(mod3) = 3Z = im(x3), exact at Z",
         "multiplication by 3 followed by mod 3"),
    ]

    _SEQUENCES_MED = [
        ("0 -> Z/2Z --(incl)--> Z/4Z --(x2)--> Z/2Z -> 0",
         True,
         "ker(x2: Z/4Z -> Z/2Z) = {0,2} = im(incl)",
         "extension of Z/2Z by Z/2Z"),
        ("0 -> A --(f)--> A+C --(proj)--> C -> 0 (split)",
         True,
         "split: section s: C -> A+C, s(c) = (0,c)",
         "direct sum gives split exact sequence"),
        ("0 -> Z --(x6)--> Z --(mod6)--> Z/6Z -> 0",
         True,
         "ker(mod6) = 6Z = im(x6)",
         "cyclic quotient exact sequence"),
    ]

    _SEQUENCES_HARD = [
        ("0 -> Z --(x2)--> Z --(mod3)--> Z/3Z -> 0",
         False,
         "ker(mod3) = 3Z but im(x2) = 2Z, 3Z != 2Z",
         "not exact: images and kernels don't match"),
        ("0 -> Z/2Z --(incl)--> Z/6Z --(x3)--> Z/3Z",
         False,
         "need to check if im(incl) = ker(x3)",
         "ker(x3) = {0,2,4} in Z/6Z, im(incl) = {0,3}, not equal"),
        ("0 -> Z --(diag)--> Z+Z --(diff)--> Z -> 0",
         True,
         "diag(n)=(n,n), diff(a,b)=a-b, ker(diff)=diag(Z)",
         "diagonal-difference exact sequence"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "abelian_category"

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
            difficulty: Controls sequence complexity.

        Returns:
            Task description string.
        """
        return "verify exactness of sequence in abelian category"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an abelian category exactness problem.

        Args:
            difficulty: Controls sequence type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = self._SEQUENCES_EASY
        elif difficulty <= 6:
            pool = self._SEQUENCES_EASY + self._SEQUENCES_MED
        else:
            pool = self._SEQUENCES_EASY + self._SEQUENCES_MED + self._SEQUENCES_HARD

        desc, exact, check, reason = self._rng.choice(pool)
        problem = f"{desc}. Is this sequence exact?"
        return problem, {
            "desc": desc, "exact": exact,
            "check": check, "reason": reason,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate exactness verification steps.

        Args:
            data: Solution data.

        Returns:
            Steps checking kernel = image at each position.
        """
        exact_str = "YES" if data["exact"] else "NO"
        return [
            f"sequence: {data['desc']}",
            "exact at B iff ker(g) = im(f)",
            data["check"],
            data["reason"],
            f"exact: {exact_str}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return exactness verdict.

        Args:
            data: Solution data.

        Returns:
            Whether the sequence is exact.
        """
        if data["exact"]:
            return "exact sequence"
        return "NOT exact"
