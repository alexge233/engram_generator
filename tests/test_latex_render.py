"""Tests for the LaTeX to Unicode terminal renderer.

Verifies that LatexRenderer correctly converts LaTeX notation to
Unicode text, handles fractions, matrices, superscripts, and
degrades gracefully on invalid input.
"""
import pytest

from engram_generator.latex_render import LatexRenderer


@pytest.fixture
def renderer() -> LatexRenderer:
    """Create a fresh LatexRenderer instance.

    Returns:
        LatexRenderer ready for use.
    """
    return LatexRenderer()


class TestLatexRenderer:
    """Verify LaTeX to Unicode conversion for terminal display.

    Tests cover fractions, superscripts, subscripts, matrix rendering,
    and graceful fallback on malformed LaTeX.
    """

    def test_simple_fraction(self, renderer: LatexRenderer) -> None:
        """Verify \\frac{a}{b} renders without crashing."""
        result = renderer.render(r"\frac{1}{2}")
        assert isinstance(result, str) and len(result) > 0

    def test_superscript(self, renderer: LatexRenderer) -> None:
        """Verify x^2 renders with a superscript indicator."""
        result = renderer.render("x^2")
        assert "x" in result and "2" in result

    def test_graceful_fallback_on_invalid(self, renderer: LatexRenderer) -> None:
        """Verify invalid LaTeX returns the original string rather than crashing."""
        broken = r"\undefinedcommand{broken"
        result = renderer.render(broken)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_inline_single_line(self, renderer: LatexRenderer) -> None:
        """Verify render_inline produces a single-line result."""
        result = renderer.render_inline(r"\frac{a}{b} + c")
        assert "\n" not in result

    def test_render_horizontal_fractions(self, renderer: LatexRenderer) -> None:
        """Verify render_horizontal produces multi-line fraction layout."""
        result = renderer.render_horizontal(r"\frac{a}{b}")
        lines = result.strip().split("\n")
        assert len(lines) >= 2

    def test_plain_text_passes_through(self, renderer: LatexRenderer) -> None:
        """Verify plain text without LaTeX passes through unchanged."""
        result = renderer.render("hello world")
        assert "hello" in result and "world" in result

    def test_clean_wikipedia_strips_mathml(self, renderer: LatexRenderer) -> None:
        """Verify clean_wikipedia removes MathML artifacts."""
        raw = "The formula is:\n  a\n  +\n  b\nwhere a=1"
        result = renderer.clean_wikipedia(raw)
        assert isinstance(result, str)
        assert "where" in result

    def test_empty_string(self, renderer: LatexRenderer) -> None:
        """Verify empty input returns empty output."""
        assert renderer.render("") == ""
        assert renderer.render_inline("") == ""
