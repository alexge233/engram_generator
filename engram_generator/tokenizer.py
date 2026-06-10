"""Character-level tokenizer for the engram generator curriculum."""
from engram_generator.base import STEP_TOKEN


class CharTokenizer:
    """Character-level tokenizer with LaTeX support.

    Every character is its own token. Supports digits, lowercase letters,
    operators, LaTeX symbols, and special structural tokens.

    Attributes:
        vocab_size: Total number of tokens including special tokens.
        pad_token_id: ID of the padding token.
        eos_token_id: ID of the end-of-sequence token.
        step_token_id: ID of the step boundary token.
    """

    PAD = "<pad>"
    EOS = "<eos>"
    STEP = STEP_TOKEN

    CHARS = list(
        "0123456789"
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        " +-/*^()[]{}=:;?.,\\_|!&~'<>%#@\""
        "$°×—→∩∪"
        "≤≥≠≈∞√∂∫∈⊂∅"
        "∀∃¬∧∨⊢⊨↔⊥"
        "αβγδεθλμπσφω"
    )

    def __init__(self):
        """Build the character-to-ID mapping."""
        self._tokens = [self.PAD, self.EOS, self.STEP] + self.CHARS
        self._char_to_id = {c: i for i, c in enumerate(self._tokens)}
        self._id_to_char = {i: c for c, i in self._char_to_id.items()}

    @property
    def vocab_size(self) -> int:
        """Return the total vocabulary size."""
        return len(self._tokens)

    @property
    def pad_token_id(self) -> int:
        """Return the padding token ID."""
        return self._char_to_id[self.PAD]

    @property
    def eos_token_id(self) -> int:
        """Return the end-of-sequence token ID."""
        return self._char_to_id[self.EOS]

    @property
    def step_token_id(self) -> int:
        """Return the step boundary token ID."""
        return self._char_to_id[self.STEP]

    def encode(self, text: str) -> list[int]:
        """Convert text to token IDs, handling <step> as a single token.

        Args:
            text: Input string to tokenize.

        Returns:
            List of integer token IDs with EOS appended.
        """
        ids = []
        i = 0
        while i < len(text):
            if text[i:i + len(STEP_TOKEN)] == STEP_TOKEN:
                ids.append(self.step_token_id)
                i += len(STEP_TOKEN)
            elif text[i] in self._char_to_id:
                ids.append(self._char_to_id[text[i]])
                i += 1
            else:
                i += 1
        ids.append(self.eos_token_id)
        return ids

    def decode(self, ids: list[int]) -> str:
        """Convert token IDs back to text.

        Args:
            ids: List of integer token IDs.

        Returns:
            Decoded string with special tokens removed (except <step>).
        """
        chars = []
        for i in ids:
            if i == self.pad_token_id or i == self.eos_token_id:
                continue
            if i == self.step_token_id:
                chars.append(STEP_TOKEN)
            else:
                chars.append(self._id_to_char.get(i, ""))
        return "".join(chars)

    def get_step_mask(self, ids: list[int]) -> list[bool]:
        """Return mask indicating which positions are <step> tokens.

        Used to mask out step tokens from loss computation.

        Args:
            ids: List of token IDs.

        Returns:
            List of booleans — True where token is <step>.
        """
        return [i == self.step_token_id for i in ids]
