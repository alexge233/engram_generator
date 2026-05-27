"""LaTeX to Unicode terminal renderer using pylatexenc."""
import re

from pylatexenc.latex2text import LatexNodes2Text


class LatexRenderer:
    """Converts LaTeX notation to Unicode for terminal display.

    Uses pylatexenc for standard LaTeX commands and adds custom
    rendering for matrices with proper multi-line bracket notation.

    Example:
        >>> r = LatexRenderer()
        >>> r.render(r'\\frac{d}{dx}(3x^2)')
        'd/dx(3x²)'
    """

    def __init__(self) -> None:
        """Initialise the pylatexenc converter."""
        self._converter = LatexNodes2Text()

    def render(self, text: str) -> str:
        """Convert LaTeX text to Unicode for terminal display.

        Args:
            text: LaTeX string.

        Returns:
            Unicode-rendered string with multi-line matrices.
        """
        try:
            text = self._render_matrices(text)
            text = self._render_augmented(text)
            text = self._render_fractions(text)
            return self._converter.latex_to_text(text)
        except Exception:
            return text

    def render_inline(self, text: str) -> str:
        """Convert LaTeX to Unicode, keeping everything on one line.

        Fractions render as num/den, no stacked rendering.

        Args:
            text: LaTeX string.

        Returns:
            Single-line Unicode string.
        """
        try:
            text = self._render_inline_fractions(text)
            return self._converter.latex_to_text(text)
        except Exception:
            return text

    def render_horizontal(self, text: str) -> str:
        """Render fractions side-by-side with horizontal bars.

        Multiple fractions in the same expression are placed next to
        each other instead of stacked vertically.

        Args:
            text: LaTeX string with one or more \\frac commands.

        Returns:
            Multi-line string with fractions arranged horizontally.
        """
        try:
            return self._render_fractions_horizontal(text)
        except Exception:
            return self.render(text)

    def _render_fractions_horizontal(self, text: str) -> str:
        """Parse and render all fractions in an expression side-by-side.

        Args:
            text: LaTeX expression.

        Returns:
            Multi-line horizontal fraction layout.
        """
        segments: list[dict] = []
        remaining = text

        while remaining:
            if "\\frac{" not in remaining:
                plain = self._converter.latex_to_text(remaining).strip()
                if plain:
                    segments.append({"type": "text", "text": plain})
                break

            idx = remaining.index("\\frac{")
            before = remaining[:idx].strip()
            if before:
                plain = self._converter.latex_to_text(before).strip()
                if plain:
                    segments.append({"type": "text", "text": plain})

            num, end_num = self._extract_braced(remaining, idx + 5)
            den, end_den = self._extract_braced(remaining, end_num)
            if num is None or den is None:
                segments.append({"type": "text",
                                 "text": self._converter.latex_to_text(remaining)})
                break

            num_r = self._converter.latex_to_text(num).strip()
            den_r = self._converter.latex_to_text(den).strip()
            segments.append({"type": "frac", "num": num_r, "den": den_r})
            remaining = remaining[end_den:]

        if not any(s["type"] == "frac" for s in segments):
            return self._converter.latex_to_text(text)

        return self._compose_horizontal(segments)

    def _compose_horizontal(self, segments: list[dict]) -> str:
        """Compose fraction and text segments into three aligned lines.

        Args:
            segments: List of {"type": "frac"/"text", ...} dicts.

        Returns:
            Three-line string with numerators, bars, and denominators.
        """
        top_parts: list[str] = []
        mid_parts: list[str] = []
        bot_parts: list[str] = []

        for seg in segments:
            if seg["type"] == "frac":
                num = seg["num"]
                den = seg["den"]
                width = max(len(num), len(den))
                top_parts.append(num.center(width))
                mid_parts.append("─" * width)
                bot_parts.append(den.center(width))
            else:
                txt = f" {seg['text']} "
                top_parts.append(" " * len(txt))
                mid_parts.append(txt)
                bot_parts.append(" " * len(txt))

        top = "".join(top_parts)
        mid = "".join(mid_parts)
        bot = "".join(bot_parts)
        return f"{top}\n{mid}\n{bot}"

    def clean_wikipedia(self, text: str) -> str:
        """Strip Wikipedia MathML artifacts and render LaTeX fragments.

        Wikipedia's API returns indented single-character MathML trees
        alongside \\textstyle LaTeX lines. This collapses the trees,
        renders the LaTeX, and cleans up whitespace.

        Args:
            text: Raw Wikipedia extract text.

        Returns:
            Cleaned text with formulas rendered as Unicode.
        """
        text = self._collapse_mathml_trees(text)
        text = self._render_texstyle(text)
        text = self._render_displaystyle(text)
        text = self._join_inline_formulas(text)
        text = re.sub(r"\n\s*\n\s*\n", "\n\n", text)
        return text.strip()

    def _collapse_mathml_trees(self, text: str) -> str:
        """Collapse indented MathML fragments and displaystyle lines.

        Wikipedia returns indented single-character trees alongside
        \\displaystyle LaTeX. Both are redundant when \\textstyle is
        present. This removes the trees and renders \\displaystyle
        inline.

        Args:
            text: Raw text with MathML fragments.

        Returns:
            Text with fragment blocks removed.
        """
        lines = text.split("\n")
        cleaned: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            is_fragment = (
                len(stripped) <= 3
                and line != line.lstrip()
                and not stripped.startswith("(")
            )
            is_empty_indent = stripped == "" and line != line.lstrip()
            if is_fragment or is_empty_indent:
                i += 1
                continue
            cleaned.append(line)
            i += 1
        return "\n".join(cleaned)

    def _render_texstyle(self, text: str) -> str:
        """Render \\textstyle LaTeX fragments to Unicode.

        Uses brace-matching rather than regex to handle nested braces
        like {\\textstyle {\\frac {f(x)}{g(x)}},}.

        Args:
            text: Text containing \\textstyle commands.

        Returns:
            Text with \\textstyle fragments rendered.
        """
        marker = "{\\textstyle"
        result = text
        while marker in result:
            idx = result.index(marker)
            content, end = self._extract_braced(result, idx)
            if content is None:
                break
            inner = content[len("\\textstyle"):].strip()
            try:
                rendered = self.render(inner)
            except Exception:
                rendered = inner
            result = result[:idx] + rendered + result[end:]
        return result

    def _join_inline_formulas(self, text: str) -> str:
        """Join orphaned continuation lines back onto preceding prose.

        After MathML collapse and displaystyle rendering, fragments
        like ' of a linear transformation T' end up on their own line
        with leading whitespace. This joins them back if they look
        like inline continuations.

        Args:
            text: Text with possible orphaned formula lines.

        Returns:
            Text with continuations joined to preceding prose.
        """
        lines = text.split("\n")
        joined: list[str] = []
        for line in lines:
            stripped = line.strip()
            is_continuation = (
                stripped
                and joined
                and joined[-1].strip()
                and line != line.lstrip()
                and not stripped.startswith("Source:")
                and not stripped.startswith("URL:")
            )
            if is_continuation:
                joined[-1] = joined[-1].rstrip() + " " + stripped
            else:
                joined.append(line)
        return "\n".join(joined)

    def _render_displaystyle(self, text: str) -> str:
        """Render \\displaystyle LaTeX fragments to Unicode.

        Args:
            text: Text containing \\displaystyle commands.

        Returns:
            Text with \\displaystyle fragments rendered inline.
        """
        marker = "{\\displaystyle"
        result = text
        while marker in result:
            idx = result.index(marker)
            content, end = self._extract_braced(result, idx)
            if content is None:
                break
            inner = content[len("\\displaystyle"):].strip()
            try:
                rendered = self.render(inner)
            except Exception:
                rendered = inner
            result = result[:idx] + rendered + result[end:]
        return result

    def _render_inline_fractions(self, text: str) -> str:
        """Convert \\frac{num}{den} to single-line fraction notation.

        Uses Unicode superscript/subscript for simple fractions and
        bracketed notation for complex ones.

        Args:
            text: Input text with LaTeX frac commands.

        Returns:
            Text with all fractions rendered inline.
        """
        parts: list[str] = []
        remaining = text
        while "\\frac{" in remaining:
            idx = remaining.index("\\frac{")
            parts.append(remaining[:idx])
            num, end_num = self._extract_braced(remaining, idx + 5)
            den, end_den = self._extract_braced(remaining, end_num)
            if num is None or den is None:
                parts.append(remaining[idx:])
                remaining = ""
                break
            num_r = self._converter.latex_to_text(num).strip()
            den_r = self._converter.latex_to_text(den).strip()
            parts.append(f"[{num_r} ∕ {den_r}]")
            remaining = remaining[end_den:]
        parts.append(remaining)
        return self._converter.latex_to_text("".join(parts))

    def _render_fractions(self, text: str) -> str:
        """Convert \\frac{num}{den} to multi-line vertical fractions.

        Handles nested braces in numerator and denominator.
        Simple fractions stay inline, complex ones stack vertically.

        Args:
            text: Input text with LaTeX frac commands.

        Returns:
            Text with fractions rendered vertically.
        """
        result = text
        while "\\frac{" in result:
            idx = result.index("\\frac{")
            num, end_num = self._extract_braced(result, idx + 5)
            den, end_den = self._extract_braced(result, end_num)
            if num is None or den is None:
                break
            replacement = self._format_fraction_parts(num, den)
            result = result[:idx] + replacement + result[end_den:]
        return result

    def _extract_braced(self, text: str, start: int) -> tuple:
        """Extract content between matching braces.

        Args:
            text: Full text.
            start: Position of opening brace.

        Returns:
            Tuple of (content, position_after_closing_brace) or (None, start).
        """
        if start >= len(text) or text[start] != "{":
            return None, start
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return text[start + 1:i], i + 1
        return None, start

    def _format_fraction_parts(self, num: str, den: str) -> str:
        """Format extracted numerator and denominator.

        Args:
            num: Raw numerator LaTeX.
            den: Raw denominator LaTeX.

        Returns:
            Formatted fraction string.
        """
        num_rendered = self._converter.latex_to_text(num)
        den_rendered = self._converter.latex_to_text(den)

        if len(num_rendered) <= 2 and len(den_rendered) <= 2:
            return self._inline_fraction(num_rendered, den_rendered)

        return self._stacked_fraction(num_rendered, den_rendered)

    def _format_fraction(self, match: re.Match) -> str:
        """Format a single fraction as vertical or inline.

        Args:
            match: Regex match with numerator and denominator groups.

        Returns:
            Formatted fraction string.
        """
        num = match.group(1).strip()
        den = match.group(2).strip()

        num_rendered = self._converter.latex_to_text(num)
        den_rendered = self._converter.latex_to_text(den)

        if len(num_rendered) <= 2 and len(den_rendered) <= 2:
            return self._inline_fraction(num_rendered, den_rendered)

        return self._stacked_fraction(num_rendered, den_rendered)

    def _inline_fraction(self, num: str, den: str) -> str:
        """Format a simple fraction inline using Unicode.

        Args:
            num: Rendered numerator.
            den: Rendered denominator.

        Returns:
            Inline fraction string.
        """
        simple = {
            ("1", "2"): "½", ("1", "3"): "⅓", ("2", "3"): "⅔",
            ("1", "4"): "¼", ("3", "4"): "¾", ("1", "5"): "⅕",
            ("1", "6"): "⅙", ("1", "8"): "⅛",
        }
        key = (num, den)
        if key in simple:
            return simple[key]
        return f"{num}/{den}"

    def _stacked_fraction(self, num: str, den: str) -> str:
        """Format a complex fraction as vertically stacked lines.

        Args:
            num: Rendered numerator.
            den: Rendered denominator.

        Returns:
            Multi-line fraction with horizontal bar.
        """
        width = max(len(num), len(den))
        bar = "─" * (width + 2)
        num_centered = num.center(width + 2)
        den_centered = den.center(width + 2)
        return f"\n{num_centered}\n{bar}\n{den_centered}\n"

    def _render_matrices(self, text: str) -> str:
        """Convert pmatrix/bmatrix to multi-line bracket notation.

        Args:
            text: Input text with LaTeX matrix commands.

        Returns:
            Text with matrices rendered as multi-line bracketed grids.
        """
        pattern = r"\\begin\{[pb]matrix\}(.*?)\\end\{[pb]matrix\}"
        return re.sub(pattern, self._format_matrix, text, flags=re.DOTALL)

    def _render_augmented(self, text: str) -> str:
        """Convert augmented matrix arrays to multi-line notation.

        Args:
            text: Input text with LaTeX array commands.

        Returns:
            Text with augmented matrices rendered.
        """
        pattern = r"\\left\(\\begin\{array\}.*?\}(.*?)\\end\{array\}\\right\)"
        return re.sub(pattern, self._format_matrix, text, flags=re.DOTALL)

    def _format_matrix(self, match: re.Match) -> str:
        """Format a matrix body into multi-line bracketed rows.

        Args:
            match: Regex match containing the matrix body.

        Returns:
            Multi-line string with Unicode box-drawing brackets.
        """
        body = match.group(1).strip()
        rows = self._parse_rows(body)
        if not rows:
            return match.group(0)
        return self._draw_matrix(rows)

    def _parse_rows(self, body: str) -> list[list[str]]:
        """Parse matrix body into a 2D list of cell strings.

        Args:
            body: Raw matrix body text.

        Returns:
            List of rows, each a list of cell strings.
        """
        raw_rows = re.split(r"\\\\", body)
        rows: list[list[str]] = []
        for row in raw_rows:
            cells = [c.strip() for c in row.split("&")]
            if any(c for c in cells):
                rows.append(cells)
        return rows

    def _draw_matrix(self, rows: list[list[str]]) -> str:
        """Draw a matrix with Unicode box-drawing characters.

        Args:
            rows: 2D list of cell strings.

        Returns:
            Multi-line matrix string.
        """
        col_widths = self._compute_widths(rows)
        lines: list[str] = []

        top = "┌ " + "  ".join(" " * w for w in col_widths) + " ┐"
        lines.append(top)

        for row in rows:
            cells = []
            for j, cell in enumerate(row):
                width = col_widths[j] if j < len(col_widths) else 6
                cells.append(cell.rjust(width))
            lines.append("│ " + "  ".join(cells) + " │")

        bottom = "└ " + "  ".join(" " * w for w in col_widths) + " ┘"
        lines.append(bottom)

        return "\n".join(lines)

    def _compute_widths(self, rows: list[list[str]]) -> list[int]:
        """Compute column widths for matrix alignment.

        Args:
            rows: 2D list of cell strings.

        Returns:
            List of maximum widths per column.
        """
        max_cols = max(len(row) for row in rows)
        widths = [0] * max_cols
        for row in rows:
            for j, cell in enumerate(row):
                if j < max_cols:
                    widths[j] = max(widths[j], len(cell))
        return widths
