"""Bioinformatics generators -- alignment, phylogenetics, ORFs, GC content.

6 generators across tiers 4-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class BioinformaticsBase(StepGenerator):
    """Base class for bioinformatics generators with shared utilities.

    Provides DNA/RNA alphabet helpers, codon table, and scoring
    constants used across sequence analysis generators.
    """

    DNA_BASES = ["A", "T", "G", "C"]

    CODON_TABLE = {
        "ATG": "Met", "TTT": "Phe", "TTC": "Phe", "TTA": "Leu",
        "TTG": "Leu", "CTT": "Leu", "CTC": "Leu", "CTA": "Leu",
        "CTG": "Leu", "ATT": "Ile", "ATC": "Ile", "ATA": "Ile",
        "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val",
        "TCT": "Ser", "TCC": "Ser", "TCA": "Ser", "TCG": "Ser",
        "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
        "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
        "GCT": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
        "TAT": "Tyr", "TAC": "Tyr", "CAT": "His", "CAC": "His",
        "CAA": "Gln", "CAG": "Gln", "AAT": "Asn", "AAC": "Asn",
        "AAA": "Lys", "AAG": "Lys", "GAT": "Asp", "GAC": "Asp",
        "GAA": "Glu", "GAG": "Glu", "TGT": "Cys", "TGC": "Cys",
        "TGG": "Trp", "CGT": "Arg", "CGC": "Arg", "CGA": "Arg",
        "CGG": "Arg", "AGT": "Ser", "AGC": "Ser", "AGA": "Arg",
        "AGG": "Arg", "GGT": "Gly", "GGC": "Gly", "GGA": "Gly",
        "GGG": "Gly",
    }

    STOP_CODONS = {"TAA", "TAG", "TGA"}

    # Common restriction enzymes and their recognition sequences
    RESTRICTION_ENZYMES = {
        "EcoRI": "GAATTC",
        "BamHI": "GGATCC",
        "HindIII": "AAGCTT",
        "NotI": "GCGGCCGC",
        "XhoI": "CTCGAG",
        "SalI": "GTCGAC",
    }


@register
class SequenceAlignmentGenerator(BioinformaticsBase):
    """Pairwise alignment using Needleman-Wunsch on short sequences.

    Performs global alignment with match=+1, mismatch=-1, gap=-2.
    Constructs the dynamic programming table, traces back the
    optimal path, and reports the aligned sequences with score.
    """

    MATCH_SCORE = 1
    MISMATCH_SCORE = -1
    GAP_PENALTY = -2

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sequence_alignment"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["edit_distance"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "pairwise Needleman-Wunsch alignment of short DNA sequences"

    def _needleman_wunsch(self, seq1: str,
                          seq2: str) -> tuple[list[list[int]], str, str, int]:
        """Run Needleman-Wunsch global alignment algorithm.

        Args:
            seq1: First sequence string.
            seq2: Second sequence string.

        Returns:
            Tuple of (dp_table, aligned_seq1, aligned_seq2, score).
        """
        n = len(seq1)
        m = len(seq2)

        # Initialise DP table
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][0] = i * self.GAP_PENALTY
        for j in range(1, m + 1):
            dp[0][j] = j * self.GAP_PENALTY

        # Fill DP table
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    diag = dp[i - 1][j - 1] + self.MATCH_SCORE
                else:
                    diag = dp[i - 1][j - 1] + self.MISMATCH_SCORE
                up = dp[i - 1][j] + self.GAP_PENALTY
                left = dp[i][j - 1] + self.GAP_PENALTY
                dp[i][j] = max(diag, up, left)

        # Traceback
        align1 = []
        align2 = []
        i, j = n, m
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                if seq1[i - 1] == seq2[j - 1]:
                    match_val = dp[i - 1][j - 1] + self.MATCH_SCORE
                else:
                    match_val = dp[i - 1][j - 1] + self.MISMATCH_SCORE
                if dp[i][j] == match_val:
                    align1.append(seq1[i - 1])
                    align2.append(seq2[j - 1])
                    i -= 1
                    j -= 1
                    continue
            if i > 0 and dp[i][j] == dp[i - 1][j] + self.GAP_PENALTY:
                align1.append(seq1[i - 1])
                align2.append("-")
                i -= 1
            else:
                align1.append("-")
                align2.append(seq2[j - 1])
                j -= 1

        align1.reverse()
        align2.reverse()
        score = dp[n][m]

        return dp, "".join(align1), "".join(align2), score

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a sequence alignment problem.

        Creates two short DNA sequences and computes their optimal
        global alignment using Needleman-Wunsch.

        Args:
            difficulty: Controls sequence length (4-8 chars).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        length = min(3 + difficulty, 8)
        seq1 = "".join(self._rng.choice(self.DNA_BASES) for _ in range(length))

        # Create seq2 by mutating seq1 slightly
        seq2_len = max(3, length + self._rng.randint(-1, 1))
        seq2_chars = list(seq1[:seq2_len])
        num_mutations = max(1, min(difficulty // 2, seq2_len - 1))
        for _ in range(num_mutations):
            pos = self._rng.randint(0, len(seq2_chars) - 1)
            mutation_type = self._rng.choice(["sub", "del", "ins"])
            if mutation_type == "sub":
                others = [b for b in self.DNA_BASES if b != seq2_chars[pos]]
                seq2_chars[pos] = self._rng.choice(others)
            elif mutation_type == "del" and len(seq2_chars) > 3:
                seq2_chars.pop(pos)
            else:
                seq2_chars.insert(pos, self._rng.choice(self.DNA_BASES))
                if len(seq2_chars) > 8:
                    seq2_chars = seq2_chars[:8]
        seq2 = "".join(seq2_chars)

        dp, align1, align2, score = self._needleman_wunsch(seq1, seq2)

        # Format a compact DP summary (first/last row)
        dp_first_row = " ".join(str(v) for v in dp[0])
        dp_last_row = " ".join(str(v) for v in dp[-1])

        return (
            f"align {seq1} and {seq2} (match=+1, mismatch=-1, gap=-2)",
            {
                "seq1": seq1,
                "seq2": seq2,
                "align1": align1,
                "align2": align2,
                "score": score,
                "dp_first_row": dp_first_row,
                "dp_last_row": dp_last_row,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"init DP: row0 = [{sd['dp_first_row']}]",
            f"fill DP table for {sd['seq1']} vs {sd['seq2']}",
            f"last row = [{sd['dp_last_row']}]",
            f"traceback: {sd['align1']} / {sd['align2']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the optimal alignment and score.

        Args:
            sd: Solution data.

        Returns:
            Aligned sequences and alignment score.
        """
        return f"{sd['align1']} | {sd['align2']}, score={sd['score']}"


@register
class BlastEvalueGenerator(BioinformaticsBase):
    """Compute BLAST E-value from bit score, database, and query size.

    E = m * n * 2^(-S) where S is the bit score, m is database
    size (residues), and n is query length. Assesses statistical
    significance of the alignment.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "blast_evalue"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute BLAST E-value and assess significance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BLAST E-value problem.

        Creates plausible BLAST search parameters: database size,
        query length, and bit score. Computes the E-value and
        determines whether the hit is significant (E < 0.01).

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Database size in residues/bases
        db_exp = self._rng.randint(4, min(4 + difficulty, 9))
        m = self._rng.randint(1, 9) * (10 ** db_exp)

        # Query length
        n = self._rng.randint(50, 100 + difficulty * 50)

        # Bit score
        bit_score = self._rng.randint(10 + difficulty * 3, 30 + difficulty * 10)

        # E = m * n * 2^(-S)
        power_term = 2.0 ** (-bit_score)
        e_value = m * n * power_term
        e_value = round(e_value, 4)

        significant = e_value < 0.01

        problem = (
            f"BLAST search: db size m={m}, query length n={n}, "
            f"bit score S={bit_score}. Compute E-value."
        )

        return problem, {
            "m": m,
            "n": n,
            "bit_score": bit_score,
            "power_term": round(power_term, 4),
            "mn": m * n,
            "e_value": e_value,
            "significant": significant,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        sig_str = "significant" if sd["significant"] else "not significant"
        return [
            "E = m * n * 2^(-S)",
            f"2^(-{sd['bit_score']}) = {sd['power_term']}",
            f"m * n = {sd['m']} * {sd['n']} = {sd['mn']}",
            f"E = {sd['mn']} * {sd['power_term']} = {sd['e_value']}",
            f"E {'<' if sd['significant'] else '>='} 0.01 -> {sig_str}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the E-value and significance assessment.

        Args:
            sd: Solution data.

        Returns:
            E-value and significance string.
        """
        sig = "significant" if sd["significant"] else "not significant"
        return f"E = {sd['e_value']}, {sig}"


@register
class PhyloDistanceGenerator(BioinformaticsBase):
    """Compute Jukes-Cantor evolutionary distance between two sequences.

    Uses d = -3/4 * ln(1 - 4p/3) where p is the fraction of
    differing sites between two aligned sequences. This corrects
    for multiple substitutions at the same site.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phylo_distance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Jukes-Cantor evolutionary distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Jukes-Cantor distance problem.

        Creates two aligned DNA sequences with a known number of
        differences and computes the corrected evolutionary distance.

        Args:
            difficulty: Controls sequence length and divergence.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        length = self._rng.randint(8, min(10 + difficulty * 3, 30))
        seq1 = "".join(self._rng.choice(self.DNA_BASES) for _ in range(length))

        # Create seq2 with controlled differences (p < 0.75 for JC validity)
        max_diffs = min(int(length * 0.7), length - 1)
        min_diffs = max(1, difficulty // 2)
        n_diffs = self._rng.randint(min_diffs, max(min_diffs, max_diffs))

        seq2_list = list(seq1)
        diff_positions = self._rng.sample(range(length), n_diffs)
        for pos in diff_positions:
            others = [b for b in self.DNA_BASES if b != seq2_list[pos]]
            seq2_list[pos] = self._rng.choice(others)
        seq2 = "".join(seq2_list)

        p = round(n_diffs / length, 4)
        inner = 1.0 - (4.0 * p / 3.0)

        if inner <= 0:
            # Saturated: too many differences for JC correction
            distance = float("inf")
            dist_str = "undefined (saturated)"
        else:
            distance = round(-0.75 * math.log(inner), 4)
            dist_str = str(distance)

        problem = (
            f"sequences: {seq1} and {seq2}. "
            f"Compute Jukes-Cantor distance."
        )

        return problem, {
            "seq1": seq1,
            "seq2": seq2,
            "length": length,
            "n_diffs": n_diffs,
            "p": p,
            "inner": round(inner, 4),
            "distance": distance,
            "dist_str": dist_str,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"differences = {sd['n_diffs']} out of {sd['length']} sites",
            f"p = {sd['n_diffs']}/{sd['length']} = {sd['p']}",
            f"1 - 4p/3 = 1 - 4*{sd['p']}/3 = {sd['inner']}",
        ]
        if sd["inner"] > 0:
            steps.append(
                f"d = -3/4 * ln({sd['inner']}) = {sd['dist_str']}"
            )
        else:
            steps.append("1 - 4p/3 <= 0: distance is undefined (saturated)")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Jukes-Cantor distance.

        Args:
            sd: Solution data.

        Returns:
            Distance value as string.
        """
        return f"d = {sd['dist_str']}"


@register
class GcContentGenerator(BioinformaticsBase):
    """Compute GC content percentage from a DNA sequence.

    GC% = (G + C) / (A + T + G + C) * 100. This is a fundamental
    sequence property used in genome annotation, primer design,
    and comparative genomics.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gc_content"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute GC content percentage of DNA sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a GC content problem.

        Creates a random DNA sequence and counts each base to
        compute GC%. At higher difficulty, computes GC% for a
        sliding window and identifies the region with highest GC.

        Args:
            difficulty: Controls sequence length and analysis type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        length = self._rng.randint(8, min(10 + difficulty * 4, 40))
        seq = "".join(self._rng.choice(self.DNA_BASES) for _ in range(length))

        count_a = seq.count("A")
        count_t = seq.count("T")
        count_g = seq.count("G")
        count_c = seq.count("C")
        total = count_a + count_t + count_g + count_c
        gc = count_g + count_c
        gc_pct = round(gc / total * 100, 4)

        problem = f"sequence: {seq}. Compute GC content."

        steps = [
            f"A={count_a}, T={count_t}, G={count_g}, C={count_c}",
            f"G+C = {gc}, total = {total}",
            f"GC% = {gc}/{total} * 100 = {gc_pct}%",
        ]

        if difficulty >= 6 and length >= 12:
            window = min(6, length // 2)
            best_gc = -1.0
            best_start = 0
            for start in range(length - window + 1):
                w_seq = seq[start:start + window]
                w_gc = w_seq.count("G") + w_seq.count("C")
                w_pct = round(w_gc / window * 100, 4)
                if w_pct > best_gc:
                    best_gc = w_pct
                    best_start = start
            steps.append(
                f"highest GC window ({window}bp) at pos {best_start}: "
                f"{best_gc}%"
            )

        return problem, {
            "seq": seq,
            "count_a": count_a,
            "count_t": count_t,
            "count_g": count_g,
            "count_c": count_c,
            "gc": gc,
            "total": total,
            "gc_pct": gc_pct,
            "steps": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the GC content percentage.

        Args:
            sd: Solution data.

        Returns:
            GC percentage string.
        """
        return f"GC = {sd['gc_pct']}%"


@register
class OpenReadingFrameGenerator(BioinformaticsBase):
    """Find the longest open reading frame (ORF) in a DNA sequence.

    Scans for ATG start codons, reads triplets until a stop codon
    (TAA, TAG, TGA), and reports the longest ORF found with its
    position and amino acid length.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "open_reading_frame"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["codon_translate"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find longest open reading frame in DNA sequence"

    def _build_orf_sequence(self, num_codons: int) -> str:
        """Build a valid ORF: ATG + coding codons + stop codon.

        Args:
            num_codons: Number of coding codons (excluding ATG and stop).

        Returns:
            DNA string for one complete ORF.
        """
        coding_codons = list(self.CODON_TABLE.keys())
        non_stop = [c for c in coding_codons if c not in self.STOP_CODONS]

        orf = "ATG"
        for _ in range(num_codons):
            orf += self._rng.choice(non_stop)
        stop = self._rng.choice(list(self.STOP_CODONS))
        orf += stop
        return orf

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ORF-finding problem.

        Constructs a DNA sequence with one or more embedded ORFs
        surrounded by non-coding flanking regions. The task is to
        find the longest ORF.

        Args:
            difficulty: Controls sequence complexity and ORF count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Build the main (longest) ORF
        main_codons = self._rng.randint(2, min(2 + difficulty, 7))
        main_orf = self._build_orf_sequence(main_codons)

        # Build flanking non-coding DNA (no ATG in frame)
        flank_len = self._rng.randint(3, 6) * 3
        flank_5 = ""
        for _ in range(flank_len):
            flank_5 += self._rng.choice(self.DNA_BASES)
        # Remove any accidental ATG in the flanking region
        flank_5 = flank_5.replace("ATG", "ACG")

        flank_3_len = self._rng.randint(2, 4) * 3
        flank_3 = ""
        for _ in range(flank_3_len):
            flank_3 += self._rng.choice(self.DNA_BASES)
        flank_3 = flank_3.replace("ATG", "ACG")

        full_seq = flank_5 + main_orf + flank_3

        # Scan for all ORFs to find the longest
        orfs_found = []
        for i in range(len(full_seq) - 2):
            if full_seq[i:i + 3] == "ATG":
                # Read codons until stop or end
                codons = []
                j = i + 3
                while j + 2 < len(full_seq):
                    codon = full_seq[j:j + 3]
                    if codon in self.STOP_CODONS:
                        orfs_found.append({
                            "start": i,
                            "end": j + 3,
                            "length_bp": j + 3 - i,
                            "codons": (j - i - 3) // 3,
                            "stop": codon,
                        })
                        break
                    codons.append(codon)
                    j += 3

        if not orfs_found:
            # Fallback: ensure at least one ORF exists
            return self._create_problem(max(1, difficulty - 1))

        longest = max(orfs_found, key=lambda x: x["length_bp"])
        aa_count = longest["codons"] + 1  # +1 for Met from ATG

        orf_seq = full_seq[longest["start"]:longest["end"]]

        problem = f"DNA: {full_seq}. Find the longest ORF."

        return problem, {
            "full_seq": full_seq,
            "orf_start": longest["start"],
            "orf_end": longest["end"],
            "orf_seq": orf_seq,
            "length_bp": longest["length_bp"],
            "aa_count": aa_count,
            "stop_codon": longest["stop"],
            "num_orfs": len(orfs_found),
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"scan for ATG start codons",
            f"found {sd['num_orfs']} ORF(s)",
            f"longest ORF at position {sd['orf_start']}: {sd['orf_seq']}",
            f"length = {sd['length_bp']} bp, "
            f"encodes {sd['aa_count']} amino acids",
            f"stop codon: {sd['stop_codon']}",
        ]
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the longest ORF details.

        Args:
            sd: Solution data.

        Returns:
            ORF position, length, and amino acid count.
        """
        return (
            f"ORF at {sd['orf_start']}-{sd['orf_end']}, "
            f"{sd['length_bp']} bp, {sd['aa_count']} aa"
        )


@register
class RestrictionDigestGenerator(BioinformaticsBase):
    """Compute fragment sizes from restriction enzyme digestion.

    Given a DNA sequence length and a list of cut site positions,
    computes the resulting fragment sizes and sorts them by size.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "restriction_digest"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute restriction digest fragment sizes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a restriction digest problem.

        Creates a linear DNA of a given length with cut sites at
        specified positions. Computes the resulting fragment sizes
        and sorts them.

        Args:
            difficulty: Controls DNA length and number of cuts.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dna_length = self._rng.randint(
            500 + difficulty * 200, 1000 + difficulty * 500
        )

        num_cuts = self._rng.randint(2, min(2 + difficulty, 7))

        # Generate sorted, unique cut positions
        positions = sorted(self._rng.sample(
            range(50, dna_length - 50), num_cuts
        ))

        # Compute fragments: from 0 to first cut, between cuts, last cut to end
        boundaries = [0] + positions + [dna_length]
        fragments = []
        for k in range(len(boundaries) - 1):
            frag_size = boundaries[k + 1] - boundaries[k]
            fragments.append(frag_size)

        sorted_fragments = sorted(fragments)

        # Pick an enzyme name for flavour
        enzyme = self._rng.choice(list(self.RESTRICTION_ENZYMES.keys()))

        pos_str = ", ".join(str(p) for p in positions)
        problem = (
            f"linear DNA ({dna_length} bp) cut by {enzyme} at "
            f"positions [{pos_str}]. Compute fragment sizes."
        )

        steps = [
            f"DNA length = {dna_length} bp",
            f"cut positions: {pos_str}",
            f"boundaries: {boundaries}",
        ]
        for k in range(len(boundaries) - 1):
            steps.append(
                f"fragment {k + 1}: {boundaries[k + 1]} - "
                f"{boundaries[k]} = {fragments[k]} bp"
            )
        steps.append(
            f"sorted: {', '.join(str(f) for f in sorted_fragments)} bp"
        )

        return problem, {
            "dna_length": dna_length,
            "enzyme": enzyme,
            "positions": positions,
            "fragments": fragments,
            "sorted_fragments": sorted_fragments,
            "steps": steps,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the sorted fragment sizes.

        Args:
            sd: Solution data.

        Returns:
            Comma-separated sorted fragment sizes.
        """
        frags = ", ".join(str(f) for f in sd["sorted_fragments"])
        return f"fragments: [{frags}] bp"
