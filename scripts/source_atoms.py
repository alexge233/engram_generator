"""Script to source unsourced atoms from Wikipedia.

Fetches theorem/formula text from Wikipedia API and updates atom content
with proper citations. Run this to populate all remaining unsourced atoms.

Usage:
    python scripts/source_atoms.py
    python scripts/source_atoms.py --atom bayes_theorem
    python scripts/source_atoms.py --dry-run
    python scripts/source_atoms.py --resourc  # re-fetch all sourced atoms
"""
import argparse
import json
import os
import re
import time
import urllib.request
import urllib.parse

from engram_generator.atoms.registry import get_all_atoms, _ATOMS
from engram_generator.base import Atom

SOURCED_FILE = os.path.join(
    os.path.dirname(__file__), os.pardir,
    "engram_generator", "atoms", "sourced.py",
)


WIKIPEDIA_SEARCH_MAP = {
    "digit_root": "Digital root",
    "sorting": "Sorting algorithm",
    "caesar": "Caesar cipher",
    "run_length": "Run-length encoding",
    "basic_prob": "Probability",
    "derivative": "Derivative",
    "graph_reach": "Reachability",
    "mean": "Arithmetic mean",
    "median": "Median",
    "mode": "Mode (statistics)",
    "base_conversion": "Positional notation",
    "binary_arithmetic": "Binary number",
    "boolean_algebra": "Boolean algebra",
    "collatz": "Collatz conjecture",
    "conditional_prob": "Conditional probability",
    "cycle_detect": "Cycle detection",
    "determinant": "Determinant",
    "expected_value": "Expected value",
    "independence_test": "Independence (probability theory)",
    "integral": "Integral",
    "logic_gate_eval": "Logic gate",
    "prefix_scan": "Prefix sum",
    "rpn": "Reverse Polish notation",
    "second_derivative": "Second derivative",
    "set_operations": "Inclusion–exclusion principle",
    "std_dev": "Standard deviation",
    "variance": "Variance",
    "z_score": "Standard score",
    "bayes_theorem": "Bayes' theorem",
    "big_o": "Big O notation",
    "coin_change": "Change-making problem",
    "complex_arithmetic": "Complex number",
    "complex_modulus": "Absolute value (algebra)",
    "correlation": "Pearson correlation coefficient",
    "cross_entropy": "Cross-entropy",
    "derivative_eval": "Derivative",
    "edit_distance": "Levenshtein distance",
    "eigenvalue": "Eigenvalues and eigenvectors",
    "linear_regression": "Simple linear regression",
    "matrix_inverse": "Invertible matrix",
    "matrix_multiply": "Matrix multiplication",
    "number_base_arithmetic": "Positional notation",
    "shortest_path": "Dijkstra's algorithm",
    "sigmoid_eval": "Sigmoid function",
    "total_probability": "Law of total probability",
    "twos_complement": "Two's complement",
    "variance_dist": "Variance",
    "attention_score": "Attention (machine learning)",
    "backprop_simple": "Backpropagation",
    "binomial_dist": "Binomial distribution",
    "complex_division": "Complex number",
    "confidence_interval": "Confidence interval",
    "convolution": "Convolution",
    "euler_formula": "Euler's formula",
    "hypothesis_test": "Statistical hypothesis test",
    "info_entropy": "Entropy (information theory)",
    "limit": "Limit (mathematics)",
    "markov_chain": "Markov chain",
    "poisson_dist": "Poisson distribution",
    "polynomial_hash": "Rolling hash",
    "qubit_measure": "Measurement in quantum mechanics",
    "softmax_eval": "Softmax function",
    "vigenere": "Vigenère cipher",
    "bloch_coords": "Bloch sphere",
    "de_moivre": "De Moivre's formula",
    "diff_equation": "Separation of variables",
    "diophantine": "Bézout's identity",
    "fourier_coefficient": "Fourier series",
    "group_order": "Order (group theory)",
    "knapsack": "Knapsack problem",
    "lcs": "Longest common subsequence",
    "lis": "Longest increasing subsequence",
    "neural_forward": "Feedforward neural network",
    "partial_fractions": "Partial fraction decomposition",
    "pauli_product": "Pauli matrices",
    "polynomial_division": "Polynomial long division",
    "quadratic_residue": "Euler's criterion",
    "quantum_gate": "Quantum logic gate",
    "recurrence_solve": "Recurrence relation",
    "tensor_product": "Kronecker product",
    "topo_sort": "Topological sorting",
    "complexity_analysis": "Computational complexity theory",
    "constraint_optimisation": "Constrained optimization",
    "construct_polynomial": "Polynomial interpolation",
    "counterexample": "Counterexample",
    "derive_formula": "Mathematical proof",
    "derive_identity": "List of trigonometric identities",
    "error_correction": "Error detection and correction",
    "error_detection": "Error analysis (mathematics)",
    "estimate_magnitude": "Fermi problem",
    "generalise_sequence": "Sequence",
    "inverse_problem": "Inverse problem",
    "lagrange_multiplier": "Lagrange multiplier",
    "method_selection": "Problem solving",
    "problem_construction": "Problem solving",
    "proof_by_induction": "Mathematical induction",
    "sufficiency_analysis": "Sufficient statistic",
    "analogy_completion": "Analogy",
    "complexity_reduction": "Reduction (complexity)",
    "conjecture_generation": "Conjecture",
    "cross_domain_transfer": "Transfer learning",
    "equation_construction": "Polynomial interpolation",
    "isomorphism_detection": "Isomorphism",
    "minimal_axioms": "Independence (mathematical logic)",
    "novel_problem": "Problem solving",
    "problem_transformation": "Reduction (complexity)",
    "self_evaluation": "Metacognition",
    "solution_elegance": "Mathematical beauty",
    "algorithm_design": "Algorithm design",
    "algorithm_improvement": "Optimization (computer science)",
    "complexity_comparison": "Computational complexity theory",
    "failure_analysis": "Debugging",
    "hypothesis_design": "Experiment",
    "impossibility_proof": "Comparison sort",
    "invariant_discovery": "Invariant (mathematics)",
    "learning_bound": "Probably approximately correct learning",
    "meta_pattern": "Pattern recognition",
    "reduction": "Reduction (complexity)",
    "representation_choice": "Data structure",
    "architecture_analysis": "Computational complexity of mathematical operations",
    "capacity_bound": "Channel capacity",
    "data_prescription": "Training, validation, and test data sets",
    "efficiency_analysis": "Algorithmic efficiency",
    "emergent_capability": "Emergence",
    "failure_mode_classification": "Failure mode and effects analysis",
    "gradient_analysis": "Backpropagation",
    "loss_design": "Loss function",
    "scaling_prediction": "Neural scaling law",
    "successor_design": "Neural architecture search",
    "training_diagnosis": "Overfitting",
}


class WikipediaFetcher:
    """Fetches article extracts from Wikipedia API.

    Attributes:
        delay: Seconds between requests to be respectful.
    """

    def __init__(self, delay: float = 0.5) -> None:
        """Initialise the fetcher.

        Args:
            delay: Delay between API calls in seconds.
        """
        self._delay = delay

    def fetch_extract(self, title: str, max_chars: int = 8000) -> str | None:
        """Fetch article text from Wikipedia, truncated to max_chars.

        Fetches the full article (no exchars limit) then truncates
        to a sentence boundary near max_chars. This avoids Wikipedia's
        API silently capping exchars at ~1200 when exintro is not set.

        Args:
            title: Wikipedia article title.
            max_chars: Maximum characters to keep.

        Returns:
            Article extract text, or None if fetch failed.
        """
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": "true",
            "format": "json",
        }
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)

        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "EngramGenerator/0.1 (www.deepnet.one)",
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                extract = page.get("extract", "")
                if extract:
                    return self._truncate_at_sentence(extract, max_chars)
        except Exception:
            pass
        return None

    def _truncate_at_sentence(self, text: str, max_chars: int) -> str:
        """Truncate text at the last sentence boundary before max_chars.

        Args:
            text: Full article text.
            max_chars: Maximum character count.

        Returns:
            Truncated text ending at a sentence boundary.
        """
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars]
        last_period = truncated.rfind(". ")
        if last_period > max_chars // 2:
            return truncated[:last_period + 1]
        return truncated

    def build_url(self, title: str) -> str:
        """Build a Wikipedia article URL from a title.

        Args:
            title: Article title.

        Returns:
            Full Wikipedia URL.
        """
        encoded = urllib.parse.quote(title.replace(" ", "_"))
        return f"https://en.wikipedia.org/wiki/{encoded}"


def source_atom(atom_name: str, fetcher: WikipediaFetcher,
                dry_run: bool = False, force: bool = False) -> bool:
    """Source a single atom from Wikipedia.

    Args:
        atom_name: Name of the atom to source.
        fetcher: WikipediaFetcher instance.
        dry_run: If True, print but don't modify.
        force: If True, re-fetch even if already sourced.

    Returns:
        True if successfully sourced.
    """
    if atom_name not in _ATOMS:
        print(f"  SKIP: {atom_name} not in registry")
        return False

    atom = _ATOMS[atom_name]
    if atom.source and not force:
        print(f"  SKIP: {atom_name} already sourced")
        return True

    wiki_title = WIKIPEDIA_SEARCH_MAP.get(atom_name)
    if not wiki_title:
        print(f"  SKIP: {atom_name} no Wikipedia mapping")
        return False

    extract = fetcher.fetch_extract(wiki_title)
    if not extract:
        print(f"  FAIL: {atom_name} could not fetch '{wiki_title}'")
        return False

    url = fetcher.build_url(wiki_title)

    if dry_run:
        print(f"  DRY: {atom_name} <- '{wiki_title}' ({len(extract)} chars)")
        return True

    atom.content = extract
    atom.source = f"Wikipedia, '{wiki_title}'"
    atom.source_url = url
    print(f"  OK: {atom_name} <- '{wiki_title}' ({len(extract)} chars)")
    time.sleep(fetcher._delay)
    return True


class SourcedFileWriter:
    """Writes sourced atom data back to the sourced.py module.

    Reads the existing sourced.py and replaces each atom's content
    block with the updated in-memory content while preserving all
    other fields (atom_type, tier, domain, source, source_url).

    Attributes:
        path: Absolute path to the sourced.py file.
    """

    def __init__(self, path: str) -> None:
        """Initialise the writer.

        Args:
            path: Path to sourced.py.
        """
        self._path = os.path.abspath(path)

    @staticmethod
    def _escape_content(text: str) -> str:
        """Escape text for embedding inside triple-quoted Python strings.

        Replaces backslashes and triple-quote sequences so the content
        can be safely placed inside a triple-double-quoted string literal.

        Args:
            text: Raw content text.

        Returns:
            Escaped text safe for triple-quoted strings.
        """
        text = text.replace("\\", "\\\\")
        text = text.replace('"""', '\\"\\"\\"')
        return text

    def write(self, atom_names: list[str]) -> int:
        """Rewrite sourced.py with updated content for the given atoms.

        Reads the existing file and replaces the content=triple-quoted
        block for each atom whose name appears in atom_names.

        Args:
            atom_names: List of atom names that were updated.

        Returns:
            Number of atoms whose content was replaced.
        """
        with open(self._path, "r", encoding="utf-8") as fh:
            text = fh.read()

        replaced = 0
        for name in atom_names:
            if name not in _ATOMS:
                continue
            atom = _ATOMS[name]

            # Match: name="<name>",\n    content="""...""",
            # The pattern finds the content block following the name field.
            # We use DOTALL to match across newlines.
            pattern = (
                r'(name="' + re.escape(name) + r'",\s*'
                r'content=""")'       # group 1: prefix up to opening quotes
                r'(.*?)'              # group 2: old content (non-greedy)
                r'(""",)'             # group 3: closing quotes + comma
            )
            match = re.search(pattern, text, re.DOTALL)
            if not match:
                print(f"  WARN: could not find content block for '{name}' "
                      f"in sourced.py")
                continue

            escaped = self._escape_content(atom.content)
            new_block = match.group(1) + escaped + match.group(3)
            text = text[:match.start()] + new_block + text[match.end():]
            replaced += 1

        with open(self._path, "w", encoding="utf-8") as fh:
            fh.write(text)

        return replaced


def main() -> None:
    """Run the atom sourcing pipeline."""
    parser = argparse.ArgumentParser(description="Source atoms from Wikipedia")
    parser.add_argument("--atom", type=str, default=None,
                        help="Source a specific atom")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be fetched without modifying")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Delay between API calls")
    parser.add_argument("--resourc", action="store_true",
                        help="Re-fetch all sourced atoms (fix truncation)")
    args = parser.parse_args()

    fetcher = WikipediaFetcher(delay=args.delay)
    atoms = get_all_atoms()

    if args.resourc:
        targets = [a for a in atoms
                   if a.name in WIKIPEDIA_SEARCH_MAP]
    else:
        targets = [a for a in atoms if not a.source]

    print(f"Total atoms: {len(atoms)}")
    print(f"Targets: {len(targets)}")
    print()

    if args.atom:
        source_atom(args.atom, fetcher, args.dry_run, force=args.resourc)
        return

    sourced_count = 0
    updated_names: list[str] = []
    for atom in targets:
        success = source_atom(atom.name, fetcher, args.dry_run,
                              force=args.resourc)
        if success:
            sourced_count += 1
            if not args.dry_run:
                updated_names.append(atom.name)

    print(f"\nSourced: {sourced_count}/{len(targets)}")

    if updated_names and not args.dry_run:
        print(f"\nWriting {len(updated_names)} atoms to sourced.py ...")
        writer = SourcedFileWriter(SOURCED_FILE)
        written = writer.write(updated_names)
        print(f"Persisted: {written}/{len(updated_names)} atoms")


if __name__ == "__main__":
    main()
