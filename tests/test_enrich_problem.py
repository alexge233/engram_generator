"""Tests for the _enrich_problem mechanism and per-generator domain knowledge fixes.

Covers the base class enrichment helpers (_enrich_problem, _val_in_text,
_significand, _list_appears_in, _format_list) and verifies that generators
with domain-specific data embed it in the problem field.
"""
import re
from fractions import Fraction

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import get_generator


class TestSignificand:
    """Tests for StepGenerator._significand extraction."""

    def test_scientific_notation_small(self) -> None:
        """Verify significand is extracted from very small floats."""
        assert StepGenerator._significand(6.674e-11) == "6.674"

    def test_scientific_notation_large(self) -> None:
        """Verify significand is extracted from very large floats."""
        assert StepGenerator._significand(1.989e30) == "1.989"

    def test_normal_range_returns_empty(self) -> None:
        """Verify empty string for values in the normal range."""
        assert StepGenerator._significand(3.14) == ""
        assert StepGenerator._significand(100.0) == ""

    def test_zero_returns_empty(self) -> None:
        """Verify empty string for zero."""
        assert StepGenerator._significand(0.0) == ""

    def test_integer_returns_empty(self) -> None:
        """Verify empty string for non-float values."""
        assert StepGenerator._significand(42) == ""


class TestValInText:
    """Tests for StepGenerator._val_in_text numeric matching."""

    def test_exact_match(self) -> None:
        """Verify exact string match works."""
        assert StepGenerator._val_in_text(3.14, "3.14", "x = 3.14 m")

    def test_absolute_value_match(self) -> None:
        """Verify matching via absolute value."""
        assert StepGenerator._val_in_text(-25.0, "-25.0", "offset is 25.0")

    def test_no_short_abs_match(self) -> None:
        """Verify single-char absolute values are not falsely matched."""
        assert not StepGenerator._val_in_text(-2, "-2", "J=2")

    def test_float_to_int_match(self) -> None:
        """Verify float-to-int matching for large values."""
        assert StepGenerator._val_in_text(1000.0, "1000.0", "n = 1000 items")

    def test_float_to_int_rejects_small(self) -> None:
        """Verify float-to-int matching rejects small values like 1.0 and 2.0."""
        assert not StepGenerator._val_in_text(1.0, "1.0", "x = 1 + 2")
        assert not StepGenerator._val_in_text(2.0, "2.0", "x = 1 + 2")

    def test_significand_match(self) -> None:
        """Verify significand matching for scientific notation values."""
        assert StepGenerator._val_in_text(
            6.674e-11, "6.674e-11",
            "G = 6.674 \\times 10^{-11}",
        )

    def test_no_match_returns_false(self) -> None:
        """Verify False when value is not present in any form."""
        assert not StepGenerator._val_in_text(99.5, "99.5", "no numbers here")

    def test_digit_boundary_rejects_embedded(self) -> None:
        """Verify 25 does not match inside 125."""
        assert not StepGenerator._val_in_text(25, "25", "x = 125 + 3")

    def test_digit_boundary_accepts_standalone(self) -> None:
        """Verify 25 matches when standalone."""
        assert StepGenerator._val_in_text(25, "25", "x = 25 + 3")


class TestFormatList:
    """Tests for StepGenerator._format_list display formatting."""

    def test_plain_numbers(self) -> None:
        """Verify plain numeric lists are formatted correctly."""
        result = StepGenerator._format_list([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_fractions_use_slash_notation(self) -> None:
        """Verify Fraction objects are formatted as n/d, not Fraction(n, d)."""
        result = StepGenerator._format_list([Fraction(1, 4), Fraction(3, 4)])
        assert result == "[1/4, 3/4]"
        assert "Fraction" not in result

    def test_nested_lists_with_fractions(self) -> None:
        """Verify nested lists with Fractions are formatted recursively."""
        result = StepGenerator._format_list([[Fraction(1, 2), 3]])
        assert result == "[[1/2, 3]]"

    def test_mixed_types(self) -> None:
        """Verify lists with mixed int, float, and Fraction values."""
        result = StepGenerator._format_list([1, 0.5, Fraction(2, 3)])
        assert result == "[1, 0.5, 2/3]"


class TestListAppearsIn:
    """Tests for StepGenerator._list_appears_in list value matching."""

    def test_numeric_list_found(self) -> None:
        """Verify matching when list values appear in step text."""
        assert StepGenerator._list_appears_in(
            [10, 20], "substitute x=10, y=20", "30",
        )

    def test_list_rejected_when_not_in_step(self) -> None:
        """Verify rejection when list values are absent from step text."""
        assert not StepGenerator._list_appears_in(
            [10, 20], "no numbers here", "30",
        )

    def test_bool_in_list_rejected(self) -> None:
        """Verify lists containing booleans are rejected."""
        assert not StepGenerator._list_appears_in(
            [True, 5], "5 in text", "result",
        )

    def test_answer_leak_rejected(self) -> None:
        """Verify lists equal to the answer string are rejected."""
        assert not StepGenerator._list_appears_in(
            [10, 20], "x=10, y=20", "[10, 20]",
        )

    def test_fraction_latex_matching(self) -> None:
        """Verify Fraction values match LaTeX \\frac notation in step text."""
        assert StepGenerator._list_appears_in(
            [Fraction(2, 5), Fraction(3, 7)],
            "P = \\frac{2}{5}, Q = \\frac{3}{7}",
            "0.6",
        )

    def test_non_meaningful_values_skipped(self) -> None:
        """Verify lists with only trivial values (0, 1, 2) are rejected."""
        assert not StepGenerator._list_appears_in(
            [0, 1, 2], "x=0, y=1, z=2", "result",
        )

    def test_long_list_rejected(self) -> None:
        """Verify lists longer than 10 elements are rejected."""
        assert not StepGenerator._list_appears_in(
            list(range(11)), "text", "answer",
        )


class TestEnrichProblem:
    """Tests for StepGenerator._enrich_problem enrichment logic."""

    def test_bare_formula_enriched_from_step1(self) -> None:
        """Verify bare formulas get values appended from step 1 assignments."""
        problem = "V = IR"
        steps = ["V=10, I=2, R=5"]
        result = StepGenerator._enrich_problem(problem, steps)
        assert "V=10" in result
        assert "I=2" in result

    def test_problem_with_numbers_not_enriched(self) -> None:
        """Verify problems already containing meaningful numbers are untouched."""
        problem = "V = IR, V=10, I=2"
        steps = ["R = 10/2 = 5"]
        result = StepGenerator._enrich_problem(problem, steps)
        assert result == problem

    def test_empty_steps_returns_original(self) -> None:
        """Verify no enrichment when steps list is empty."""
        problem = "V = IR"
        result = StepGenerator._enrich_problem(problem, [])
        assert result == problem

    def test_bool_values_not_leaked(self) -> None:
        """Verify boolean values in solution_data are never appended."""
        problem = "test convergence"
        steps = ["check ratio"]
        sd = {"converges": True, "ratio": 0.5}
        result = StepGenerator._enrich_problem(problem, steps, sd)
        assert "True" not in result
        assert "converges" not in result

    def test_internal_keys_excluded(self) -> None:
        """Verify keys in _INTERNAL_KEYS are not appended."""
        problem = "compute result"
        steps = ["x = 42"]
        sd = {"x": 42, "answer": 42, "root": 5, "count": 3}
        result = StepGenerator._enrich_problem(problem, steps, sd)
        assert "answer=" not in result
        assert "root=" not in result
        assert "count=" not in result

    def test_result_key_patterns_excluded(self) -> None:
        """Verify keys matching _RESULT_KEY_PATTERNS are not appended."""
        problem = "compute"
        steps = ["x = 10"]
        sd = {"x": 10, "is_stable": True, "pair_products": 5}
        result = StepGenerator._enrich_problem(problem, steps, sd)
        assert "is_stable" not in result
        assert "pair_products" not in result

    def test_scalar_fraction_enriched(self) -> None:
        """Verify scalar Fraction values are enriched when found in step text."""
        problem = "P(A|B)"
        steps = ["P(A|B) = \\frac{1}{3}"]
        sd = {"p_ab": Fraction(1, 3)}
        result = StepGenerator._enrich_problem(problem, steps, sd)
        assert "p_ab=1/3" in result

    def test_list_values_formatted_cleanly(self) -> None:
        """Verify list values in enrichment use clean Fraction formatting."""
        problem = "P(A)"
        steps = ["P = \\frac{2}{5} * \\frac{3}{7}"]
        sd = {"probs": [Fraction(2, 5), Fraction(3, 7)]}
        result = StepGenerator._enrich_problem(problem, steps, sd)
        if "probs=" in result:
            assert "Fraction" not in result

    def test_answer_value_not_leaked_via_fallback(self) -> None:
        """Verify solution_data values equal to the answer are not appended.

        The answer-leak guard uses the explicit ``answer`` parameter
        passed from ``_generate_one``.
        """
        problem = "compute F"
        steps = ["substitute (100)(9.8) = 980"]
        sd = {"m": 100, "g": 9.8}
        result = StepGenerator._enrich_problem(problem, steps, sd, answer="980")
        assert "m=100" in result
        assert "g=9.8" in result

    def test_answer_leak_blocked_without_sd_answer_key(self) -> None:
        """Verify leak guard works even when solution_data has no 'answer' key.

        Before the fix, the guard relied on ``solution_data.get('answer')``,
        which was often empty. Now it uses the explicit ``answer`` parameter.
        """
        problem = "compute F"
        steps = ["substitute (100)(9.8) = 980"]
        sd = {"m": 100, "g": 9.8, "F": 980}
        result = StepGenerator._enrich_problem(problem, steps, sd, answer="980")
        assert "F=980" not in result
        assert "m=100" in result


class TestGeneratorDomainKnowledge:
    """Tests that generators embed domain knowledge in the problem field.

    Each test verifies that a specific generator's ``_create_problem``
    includes the reference data a from-scratch model needs to solve it,
    rather than deferring that data to step 1.
    """

    def test_molar_mass_includes_atomic_masses(self) -> None:
        """Verify molar_mass embeds atomic mass values in the problem."""
        gen = get_generator("molar_mass")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            for elem, _ in sd["parts"]:
                assert elem + "=" in problem, (
                    f"molar_mass problem missing mass for {elem}: {problem}"
                )

    def test_dihybrid_cross_includes_phenotypes(self) -> None:
        """Verify dihybrid_cross embeds phenotype names in the problem."""
        gen = get_generator("dihybrid_cross")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            _, _, dn1, rn1 = sd["trait1"]
            assert dn1 in problem, f"missing dominant phenotype: {problem}"
            assert rn1 in problem, f"missing recessive phenotype: {problem}"

    def test_genetic_code_redundancy_includes_codons(self) -> None:
        """Verify genetic_code_redundancy lists codons in the problem."""
        gen = get_generator("genetic_code_redundancy")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            for aa in sd["query_aas"]:
                assert aa in problem
            assert re.search(r"[AUGC]{3}", problem), (
                f"problem missing codon sequences: {problem}"
            )

    def test_hybridisation_includes_bond_counts(self) -> None:
        """Verify hybridisation embeds bond and lone pair counts."""
        gen = get_generator("hybridisation")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            assert f"bonds={sd['bonds']}" in problem
            assert f"lone_pairs={sd['lone_pairs']}" in problem

    def test_heat_treatment_rank_includes_hardness(self) -> None:
        """Verify heat_treatment rank mode includes HRC ranges."""
        gen = get_generator("heat_treatment")
        gen.set_difficulty(7, 8)
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            if sd["mode"] == "rank":
                assert "HRC" in problem, f"rank mode missing HRC data: {problem}"

    def test_molecular_orbital_includes_electrons(self) -> None:
        """Verify molecular_orbital_diagram includes total electron count."""
        gen = get_generator("molecular_orbital_diagram")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            total_e = sd["mol"]["total_e"]
            assert str(total_e) in problem, (
                f"MO diagram missing electron count {total_e}: {problem}"
            )

    def test_schwarzschild_includes_mass(self) -> None:
        """Verify schwarzschild_metric includes mass in the problem."""
        gen = get_generator("schwarzschild_metric")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            assert "M=" in problem, f"missing mass: {problem}"
            assert "G=" in problem or "6.674" in problem, (
                f"missing gravitational constant: {problem}"
            )

    def test_phase_space_includes_potential(self) -> None:
        """Verify phase_space includes V(q) expression in the problem."""
        gen = get_generator("phase_space")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            assert "V(q)" in problem, f"missing V(q): {problem}"
            assert sd["V_str"] in problem, (
                f"V_str '{sd['V_str']}' not in problem: {problem}"
            )

    def test_hamiltonian_includes_lagrangian(self) -> None:
        """Verify hamiltonian includes the Lagrangian expression."""
        gen = get_generator("hamiltonian")
        for _ in range(5):
            difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
            problem, sd = gen._create_problem(difficulty)
            assert "L =" in problem or "L=" in problem, (
                f"missing Lagrangian: {problem}"
            )
            assert str(sd["a"]) in problem, (
                f"missing kinetic coefficient a={sd['a']}: {problem}"
            )


class TestEnrichNoLeaks:
    """Tests that enrichment never leaks answers or derived values.

    Runs a broad sample across all generators to verify the enrichment
    mechanism does not introduce the final answer or internal keys
    into the problem field.
    """

    def test_no_enrichment_leaks_keyword_answers(self) -> None:
        """Verify enrichment does not leak keyword answers like True/False."""
        from engram_generator.curriculum.registry import get_all_generators

        keywords = {"converges", "diverges", "true", "false", "stable", "unstable"}
        violations = []

        for gen in get_all_generators():
            for _ in range(3):
                difficulty = gen._rng.randint(gen._min_difficulty, gen._max_difficulty)
                try:
                    original, sd = gen._create_problem(difficulty)
                    steps = gen._create_steps(sd)
                    answer = gen._create_answer(sd)
                    enriched = gen._enrich_problem(original, steps, sd)

                    if enriched == original:
                        continue

                    added = enriched[len(original):].lower()
                    answer_lower = str(answer).strip().lower()

                    for kw in keywords:
                        if kw in answer_lower and kw in added:
                            violations.append(
                                f"{gen.task_name}: leaked '{kw}' "
                                f"(answer={answer})"
                            )
                except Exception:
                    continue

        assert not violations, (
            f"{len(violations)} keyword leaks:\n" + "\n".join(violations[:10])
        )
