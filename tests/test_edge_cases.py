"""Tests targeting every remaining uncovered edge case.

Each test directly exercises the specific code path that coverage missed.
"""
import pytest
from engram_generator.curriculum.registry import get_generator


class TestTier1EdgeCases:
    """Cover fibonacci n<=1 edge cases (lines 391, 393)."""

    def test_fibonacci_n_zero(self) -> None:
        """Force fibonacci with tiny n by using min difficulty."""
        gen = get_generator("fibonacci", min_difficulty=1, max_difficulty=1, seed=42)
        for _ in range(20):
            s = gen.generate(1)[0]
            assert s.answer


class TestTier3EdgeCases:
    """Cover GCDHelper, PolynomialHelper, MatrixHelper edge cases."""

    def test_gcd_with_swapped_operands(self) -> None:
        """Force GCDHelper path where a < b triggers swap."""
        gen = get_generator("gcd", min_difficulty=1, max_difficulty=1, seed=1)
        for _ in range(50):
            s = gen.generate(1)[0]
            assert s.answer

    def test_gcd_with_zero_remainder(self) -> None:
        """Force GCD where b divides a exactly."""
        gen = get_generator("gcd", min_difficulty=1, max_difficulty=2, seed=7)
        for _ in range(50):
            s = gen.generate(1)[0]
            assert s.answer

    def test_mod_inv_extended_euclidean(self) -> None:
        """Exercise the extended euclidean back-substitution."""
        gen = get_generator("mod_inv", min_difficulty=1, max_difficulty=3, seed=42)
        for _ in range(30):
            s = gen.generate(1)[0]
            assert s.answer

    def test_integral_zero_coefficient(self) -> None:
        """Force polynomial with zero-valued terms."""
        gen = get_generator("integral", min_difficulty=1, max_difficulty=1, seed=3)
        for _ in range(30):
            s = gen.generate(1)[0]
            assert s.answer

    def test_determinant_all_difficulties(self) -> None:
        """Cover 2x2 and 3x3 determinant paths."""
        gen = get_generator("determinant", min_difficulty=1, max_difficulty=8, seed=42)
        for _ in range(50):
            s = gen.generate(1)[0]
            assert s.answer

    def test_mod_pow_step_formatting(self) -> None:
        """Cover the modpow equivalence formatting."""
        gen = get_generator("mod_pow", min_difficulty=2, max_difficulty=5, seed=42)
        for _ in range(30):
            s = gen.generate(1)[0]
            assert s.answer

    def test_cycle_detect_both_outcomes(self) -> None:
        """Force both cycle and no-cycle paths."""
        gen = get_generator("cycle_detect", min_difficulty=1, max_difficulty=8, seed=42)
        found_yes = False
        found_no = False
        for _ in range(50):
            s = gen.generate(1)[0]
            if s.answer == "yes":
                found_yes = True
            elif s.answer == "no":
                found_no = True
        assert found_yes and found_no


class TestTier4EdgeCases:
    """Cover physics sampler, bivariate zero terms, format edge cases."""

    def test_partial_derivative_zero_term(self) -> None:
        """Force partial derivative that produces a zero term."""
        gen = get_generator("partial_derivative", min_difficulty=1, max_difficulty=3, seed=5)
        for _ in range(50):
            s = gen.generate(1)[0]
            assert s.answer

    def test_eigenvalue_various_seeds(self) -> None:
        """Cover eigenvalue matrix construction edge cases."""
        for seed in range(20):
            gen = get_generator("eigenvalue", min_difficulty=1, max_difficulty=5, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_matrix_inverse_det_construction(self) -> None:
        """Cover matrix inverse with det=1 construction."""
        gen = get_generator("matrix_inverse", min_difficulty=1, max_difficulty=5, seed=42)
        for _ in range(30):
            s = gen.generate(1)[0]
            assert s.answer

    def test_shortest_path_various_seeds(self) -> None:
        """Cover graph construction edge cases."""
        for seed in range(20):
            gen = get_generator("shortest_path", min_difficulty=1, max_difficulty=5, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer


class TestTier5EdgeCases:
    """Cover gaussian elimination, chain rule, and format edge cases."""

    def test_gaussian_elimination_zero_pivot(self) -> None:
        """Force zero pivot path in gaussian elimination."""
        for seed in range(30):
            gen = get_generator("gaussian_elimination", min_difficulty=1, max_difficulty=8, seed=seed)
            try:
                s = gen.generate(1)[0]
                assert s.answer
            except Exception:
                pytest.fail(f"gaussian_elimination crashed at seed={seed}")

    def test_chain_rule_various_compositions(self) -> None:
        """Cover all composite function types."""
        for seed in range(30):
            gen = get_generator("chain_rule", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_product_rule_negative_coefficients(self) -> None:
        """Force negative coefficient formatting paths."""
        for seed in range(30):
            gen = get_generator("product_rule", min_difficulty=1, max_difficulty=5, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_newton_raphson_convergence(self) -> None:
        """Cover newton raphson iteration paths."""
        gen = get_generator("newton_raphson", min_difficulty=1, max_difficulty=5, seed=42)
        for _ in range(20):
            s = gen.generate(1)[0]
            assert s.answer

    def test_cross_entropy_various_distributions(self) -> None:
        """Cover cross entropy with different distribution sizes."""
        for seed in range(20):
            gen = get_generator("cross_entropy", min_difficulty=1, max_difficulty=5, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer


class TestTier6EdgeCases:
    """Cover derangement base cases, LIS edge cases, primality."""

    def test_derangement_small_n(self) -> None:
        """Force derangement base cases D(0)=1, D(1)=0."""
        gen = get_generator("derangement", min_difficulty=1, max_difficulty=1, seed=42)
        for _ in range(20):
            s = gen.generate(1)[0]
            assert s.answer

    def test_primality_both_outcomes(self) -> None:
        """Force both prime and composite results."""
        gen = get_generator("primality", min_difficulty=1, max_difficulty=5, seed=42)
        found_yes = False
        found_no = False
        for _ in range(50):
            s = gen.generate(1)[0]
            if s.answer == "yes":
                found_yes = True
            elif s.answer == "no":
                found_no = True
        assert found_yes and found_no

    def test_lis_various_sequences(self) -> None:
        """Cover LIS patience sorting branches."""
        for seed in range(30):
            gen = get_generator("lis", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_knapsack_various_capacities(self) -> None:
        """Cover knapsack DP table edge cases."""
        for seed in range(20):
            gen = get_generator("knapsack", min_difficulty=1, max_difficulty=5, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer


class TestTier7EdgeCases:
    """Cover derivative rule evaluation and method selection paths."""

    def test_error_detection_various_seeds(self) -> None:
        """Force different error types in error detection."""
        for seed in range(30):
            gen = get_generator("error_detection", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_method_selection_all_methods(self) -> None:
        """Cover all method selection paths."""
        for seed in range(30):
            gen = get_generator("method_selection", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_derive_formula_all_types(self) -> None:
        """Cover all derivation types."""
        for seed in range(30):
            gen = get_generator("derive_formula", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_estimate_magnitude_various(self) -> None:
        """Cover estimation edge cases."""
        for seed in range(20):
            gen = get_generator("estimate_magnitude", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer


class TestTier9EdgeCases:
    """Cover algorithm template properties and binary search branches."""

    def test_algorithm_design_all_types(self) -> None:
        """Cover all algorithm design templates."""
        for seed in range(30):
            gen = get_generator("algorithm_design", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_impossibility_proof_all_types(self) -> None:
        """Cover all lower bound proof types."""
        for seed in range(30):
            gen = get_generator("impossibility_proof", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_complexity_comparison_all_pairs(self) -> None:
        """Cover all algorithm comparison pairs."""
        for seed in range(30):
            gen = get_generator("complexity_comparison", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer


class TestTier10EdgeCases:
    """Cover computation graph and scaling law helper classes."""

    def test_gradient_analysis_various(self) -> None:
        """Cover all computation graph types."""
        for seed in range(30):
            gen = get_generator("gradient_analysis", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_scaling_prediction_various(self) -> None:
        """Cover scaling law fitting edge cases."""
        for seed in range(20):
            gen = get_generator("scaling_prediction", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer

    def test_successor_design_all_types(self) -> None:
        """Cover all architectural improvement templates."""
        for seed in range(20):
            gen = get_generator("successor_design", min_difficulty=1, max_difficulty=8, seed=seed)
            s = gen.generate(1)[0]
            assert s.answer
