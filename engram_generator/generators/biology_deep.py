"""Deep biology generators -- molecular bio, evolution, population genetics, immunology.

10 generators across tiers 3-5 covering DNA replication, transcription,
translation, natural selection fitness, phylogenetic parsimony, protein
structure prediction, population growth rate, immune response binding,
allele frequency change under selection, and genetic code redundancy.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER UTILITIES
# ===================================================================

CODON_TABLE: dict[str, str] = {
    "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
    "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "UAU": "Tyr", "UAC": "Tyr", "UAA": "Stop", "UAG": "Stop",
    "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "UGU": "Cys", "UGC": "Cys", "UGA": "Stop", "UGG": "Trp",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}

DNA_COMPLEMENT: dict[str, str] = {"A": "T", "T": "A", "C": "G", "G": "C"}


def _complement(base: str) -> str:
    """Return the DNA complement of a base.

    Args:
        base: A single DNA base (A, T, C, G).

    Returns:
        Complementary base.
    """
    return DNA_COMPLEMENT[base]


def _reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence.

    Args:
        seq: DNA sequence string.

    Returns:
        Reverse complement string.
    """
    return "".join(_complement(b) for b in reversed(seq))


def _anticodon(codon: str) -> str:
    """Return the tRNA anticodon for an mRNA codon (3'->5').

    Args:
        codon: mRNA codon (3 bases, using U).

    Returns:
        Anticodon string.
    """
    rna_comp = {"A": "U", "U": "A", "C": "G", "G": "C"}
    return "".join(rna_comp[b] for b in codon)


# ===================================================================
# 1. DNA REPLICATION FORK (tier 4)
# ===================================================================

@register
class DNAReplicationForkGenerator(StepGenerator):
    """Trace DNA replication on leading and lagging strands.

    Given a template strand 5'->3', the leading strand is synthesised
    continuously (3'->5' template read as 5'->3' new strand). The
    lagging strand produces Okazaki fragments.

    Difficulty scaling:
        Difficulty 1-3: template of 9-12 bases.
        Difficulty 4-6: template of 12-18 bases.
        Difficulty 7-8: template of 18-24 bases.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dna_replication_fork"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "write the products of DNA replication on both strands"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DNA replication fork problem.

        Args:
            difficulty: Controls template length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(9, 12)
        elif difficulty <= 6:
            n = self._rng.randint(12, 18)
        else:
            n = self._rng.randint(18, 24)

        bases = "ATCG"
        template = "".join(self._rng.choice(bases) for _ in range(n))

        leading = "".join(_complement(b) for b in template)
        lagging_template = _reverse_complement(template)
        lagging = "".join(_complement(b) for b in lagging_template)

        frag_size = 3 + self._rng.randint(0, 2)
        okazaki: list[str] = []
        for i in range(0, len(lagging), frag_size):
            okazaki.append(lagging[i:i + frag_size])

        steps = [
            f"template 3'->5': {template}",
            f"leading strand 5'->3': {leading} (continuous)",
            f"lagging template 5'->3': {lagging_template}",
            f"Okazaki fragments (5'->3'): {okazaki}",
        ]

        problem = f"replicate template 3'->5': {template}"
        return problem, {
            "template": template, "leading": leading,
            "lagging_template": lagging_template,
            "okazaki": okazaki, "steps": steps,
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
        """Return both strand products.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"leading: {sd['leading']}; "
                f"Okazaki: {sd['okazaki']}")


# ===================================================================
# 2. TRANSCRIPTION PROCESS (tier 4)
# ===================================================================

@register
class TranscriptionProcessGenerator(StepGenerator):
    """Trace transcription from DNA template to mRNA.

    The template strand (3'->5') is read to produce mRNA (5'->3').
    Base pairing: A->U, T->A, C->G, G->C.

    Difficulty scaling:
        Difficulty 1-3: sequence of 9-12 bases.
        Difficulty 4-6: sequence of 12-18 bases.
        Difficulty 7-8: sequence of 18-24 bases.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transcription_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "transcribe DNA template strand to mRNA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transcription problem.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(9, 12)
        elif difficulty <= 6:
            n = self._rng.randint(12, 18)
        else:
            n = self._rng.randint(18, 24)

        bases = "ATCG"
        template = "".join(self._rng.choice(bases) for _ in range(n))

        dna_to_rna = {"A": "U", "T": "A", "C": "G", "G": "C"}
        mrna = "".join(dna_to_rna[b] for b in template)
        coding = "".join(_complement(b) for b in template)

        steps = [
            f"template strand 3'->5': {template}",
            f"coding strand 5'->3': {coding}",
            f"mRNA 5'->3': {mrna}",
        ]

        problem = f"transcribe template 3'->5': {template}"
        return problem, {
            "template": template, "coding": coding,
            "mrna": mrna, "steps": steps,
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
        """Return the mRNA product.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"mRNA 5'->3': {sd['mrna']}"


# ===================================================================
# 3. TRANSLATION ELONGATION (tier 4)
# ===================================================================

@register
class TranslationElongationGenerator(StepGenerator):
    """Translate an mRNA sequence codon by codon.

    Uses the standard genetic code. Shows each codon, its amino acid,
    and the tRNA anticodon. Translation starts at AUG.

    Difficulty scaling:
        Difficulty 1-3: 3-4 codons.
        Difficulty 4-6: 4-6 codons.
        Difficulty 7-8: 6-8 codons.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "translation_elongation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "translate mRNA codons to amino acids with anticodons"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a translation problem.

        Args:
            difficulty: Controls number of codons.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            num_codons = self._rng.randint(3, 4)
        elif difficulty <= 6:
            num_codons = self._rng.randint(4, 6)
        else:
            num_codons = self._rng.randint(6, 8)

        # Build mRNA starting with AUG, ending before a stop
        rna_bases = "AUGC"
        sense_codons = [c for c, aa in CODON_TABLE.items() if aa != "Stop"]
        codons = ["AUG"]
        for _ in range(num_codons - 1):
            codons.append(self._rng.choice(sense_codons))

        mrna = "".join(codons)
        translations: list[dict[str, str]] = []
        steps: list[str] = [f"mRNA: {mrna}"]

        for codon in codons:
            aa = CODON_TABLE[codon]
            anti = _anticodon(codon)
            translations.append({"codon": codon, "aa": aa, "anticodon": anti})
            steps.append(f"{codon} -> {aa} (anticodon: {anti})")

        protein = "-".join(t["aa"] for t in translations)
        steps.append(f"protein: {protein}")

        problem = f"translate mRNA: {mrna}"
        return problem, {
            "mrna": mrna, "codons": codons,
            "translations": translations,
            "protein": protein, "steps": steps,
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
        """Return the protein sequence.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"protein: {sd['protein']}"


# ===================================================================
# 4. NATURAL SELECTION FITNESS (tier 5)
# ===================================================================

@register
class NaturalSelectionFitnessGenerator(StepGenerator):
    """Compute allele frequency change under selection for one generation.

    Given genotype fitnesses w_AA, w_Aa, w_aa and initial allele freq p,
    computes delta_p = p*q*(p*(w_AA-w_Aa) + q*(w_Aa-w_aa)) / w_bar.

    Difficulty scaling:
        Difficulty 1-3: simple dominance (w_AA = w_Aa > w_aa).
        Difficulty 4-6: incomplete dominance.
        Difficulty 7-8: overdominance (w_Aa > w_AA, w_aa).

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "natural_selection_fitness"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute allele frequency change under natural selection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a natural selection problem.

        Args:
            difficulty: Controls fitness model.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        p = round(self._rng.uniform(0.2, 0.8), 2)
        q = round(1 - p, 4)

        if difficulty <= 3:
            w_AA = 1.0
            w_Aa = 1.0
            w_aa = round(self._rng.uniform(0.5, 0.9), 2)
        elif difficulty <= 6:
            w_AA = 1.0
            w_Aa = round(self._rng.uniform(0.8, 1.0), 2)
            w_aa = round(self._rng.uniform(0.4, 0.8), 2)
        else:
            w_AA = round(self._rng.uniform(0.7, 0.95), 2)
            w_Aa = 1.0
            w_aa = round(self._rng.uniform(0.5, 0.85), 2)

        w_bar = round(p * p * w_AA + 2 * p * q * w_Aa + q * q * w_aa, 4)
        num = p * q * (p * (w_AA - w_Aa) + q * (w_Aa - w_aa))
        delta_p = round(num / w_bar, 4) if w_bar != 0 else 0.0
        p_new = round(p + delta_p, 4)

        problem = (f"p={p}, w_AA={w_AA}, w_Aa={w_Aa}, w_aa={w_aa}; "
                   f"compute delta_p")
        return problem, {
            "p": p, "q": q, "w_AA": w_AA, "w_Aa": w_Aa, "w_aa": w_aa,
            "w_bar": w_bar, "delta_p": delta_p, "p_new": p_new,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"p = {sd['p']}, q = {sd['q']}",
            f"w_bar = p^2*w_AA + 2pq*w_Aa + q^2*w_aa = {sd['w_bar']}",
            f"delta_p = pq(p(w_AA-w_Aa) + q(w_Aa-w_aa))/w_bar = {sd['delta_p']}",
            f"p' = p + delta_p = {sd['p_new']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the frequency change.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"delta_p = {sd['delta_p']}; p' = {sd['p_new']}"


# ===================================================================
# 5. PHYLOGENETIC PARSIMONY (tier 5)
# ===================================================================

@register
class PhylogeneticParsimonyGenerator(StepGenerator):
    """Find the most parsimonious tree for aligned sequences.

    Given 3-4 taxa with aligned sequences, counts minimum substitutions
    for each possible unrooted tree topology and selects the one with
    fewest changes.

    Difficulty scaling:
        Difficulty 1-3: 3 taxa, 4 sites.
        Difficulty 4-6: 3 taxa, 6 sites.
        Difficulty 7-8: 4 taxa, 5-6 sites.

    Prerequisites:
        comparison (tier 0).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phylogenetic_parsimony"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find the most parsimonious phylogenetic tree"

    def _parsimony_score_3taxa(self, seqs: list[str]) -> dict[str, int]:
        """Compute parsimony scores for all 3-taxa topologies.

        For 3 taxa there is only one unrooted topology, but we
        consider which taxon is the outgroup.

        Args:
            seqs: List of 3 aligned sequences.

        Returns:
            Dictionary mapping topology description to score.
        """
        names = ["A", "B", "C"]
        scores: dict[str, int] = {}
        for outgroup in range(3):
            others = [i for i in range(3) if i != outgroup]
            score = 0
            for site in range(len(seqs[0])):
                bases = [seqs[i][site] for i in range(3)]
                inner = set(bases[i] for i in others)
                if len(inner) == 1:
                    if bases[outgroup] != list(inner)[0]:
                        score += 1
                else:
                    score += 1
                    if bases[outgroup] not in inner:
                        score += 1
            label = (f"({names[others[0]]},{names[others[1]]})"
                     f",{names[outgroup]}")
            scores[label] = score
        return scores

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a phylogenetic parsimony problem.

        Args:
            difficulty: Controls number of taxa and sites.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        bases = "ACGT"
        if difficulty <= 3:
            n_taxa, n_sites = 3, 4
        elif difficulty <= 6:
            n_taxa, n_sites = 3, 6
        else:
            n_taxa, n_sites = 3, self._rng.randint(5, 6)

        # Generate aligned sequences with some variation
        ancestor = [self._rng.choice(bases) for _ in range(n_sites)]
        seqs: list[str] = []
        for _ in range(n_taxa):
            seq = list(ancestor)
            mutations = self._rng.randint(1, max(1, n_sites // 2))
            for _ in range(mutations):
                pos = self._rng.randint(0, n_sites - 1)
                seq[pos] = self._rng.choice(bases)
            seqs.append("".join(seq))

        names = ["A", "B", "C"][:n_taxa]
        scores = self._parsimony_score_3taxa(seqs)

        steps: list[str] = []
        for i, name in enumerate(names):
            steps.append(f"{name}: {seqs[i]}")
        for topo, score in scores.items():
            steps.append(f"tree {topo}: {score} changes")

        best_topo = min(scores, key=scores.get)
        best_score = scores[best_topo]
        steps.append(f"most parsimonious: {best_topo} ({best_score} changes)")

        seq_desc = "; ".join(f"{n}={s}" for n, s in zip(names, seqs))
        problem = f"parsimony: {seq_desc}"
        return problem, {
            "seqs": seqs, "names": names,
            "scores": scores, "best_topo": best_topo,
            "best_score": best_score, "steps": steps,
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
        """Return the most parsimonious tree.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"best tree: {sd['best_topo']} ({sd['best_score']} substitutions)"


# ===================================================================
# 6. PROTEIN STRUCTURE (tier 4)
# ===================================================================

@register
class ProteinStructureGenerator(StepGenerator):
    """Predict secondary structure tendency from amino acid properties.

    Template-based: classifies residues as helix-preferring (A, E, L, M),
    sheet-preferring (V, I, Y, F), or coil/turn (G, P, S, N).
    Reports dominant structure for a short peptide.

    Difficulty scaling:
        Difficulty 1-3: peptide of 5-6 residues.
        Difficulty 4-6: peptide of 6-8 residues.
        Difficulty 7-8: peptide of 8-10 residues.

    Prerequisites:
        comparison (tier 0).
    """

    HELIX_PREF = {"A", "E", "L", "M", "Q", "K"}
    SHEET_PREF = {"V", "I", "Y", "F", "W", "T"}
    COIL_PREF = {"G", "P", "S", "N", "D", "R"}
    ALL_AA = list(HELIX_PREF | SHEET_PREF | COIL_PREF)

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "protein_structure"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "predict secondary structure tendency from amino acid sequence"

    def _classify(self, aa: str) -> str:
        """Classify an amino acid's secondary structure preference.

        Args:
            aa: Single-letter amino acid code.

        Returns:
            Structure class: 'helix', 'sheet', or 'coil'.
        """
        if aa in self.HELIX_PREF:
            return "helix"
        if aa in self.SHEET_PREF:
            return "sheet"
        return "coil"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a protein structure prediction problem.

        Args:
            difficulty: Controls peptide length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(5, 6)
        elif difficulty <= 6:
            n = self._rng.randint(6, 8)
        else:
            n = self._rng.randint(8, 10)

        peptide = [self._rng.choice(self.ALL_AA) for _ in range(n)]
        classifications: list[str] = []
        counts = {"helix": 0, "sheet": 0, "coil": 0}

        steps: list[str] = [f"peptide: {''.join(peptide)}"]
        for aa in peptide:
            cls = self._classify(aa)
            classifications.append(cls)
            counts[cls] += 1
            steps.append(f"{aa} -> {cls}")

        dominant = max(counts, key=counts.get)
        steps.append(f"counts: {counts}")
        steps.append(f"dominant tendency: {dominant}")

        problem = f"predict structure for {''.join(peptide)}"
        return problem, {
            "peptide": "".join(peptide), "classifications": classifications,
            "counts": counts, "dominant": dominant, "steps": steps,
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
        """Return the predicted structure tendency.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return (f"dominant: {sd['dominant']}; "
                f"helix={sd['counts']['helix']}, "
                f"sheet={sd['counts']['sheet']}, "
                f"coil={sd['counts']['coil']}")


# ===================================================================
# 7. POPULATION GROWTH RATE (tier 4)
# ===================================================================

@register
class PopulationGrowthRateGenerator(StepGenerator):
    """Compute intrinsic growth rate and doubling time.

    r = ln(N_t / N_0) / t. Doubling time T_d = ln(2) / r.

    Difficulty scaling:
        Difficulty 1-3: N_0 in [50, 200], t in [1, 5].
        Difficulty 4-6: N_0 in [100, 500], t in [3, 10].
        Difficulty 7-8: N_0 in [200, 1000], t in [5, 20].

    Prerequisites:
        logarithm (tier 5).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "population_growth_rate"

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
        return "compute intrinsic growth rate and doubling time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a population growth rate problem.

        Args:
            difficulty: Controls population and time ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n0 = self._rng.randint(50, 200)
            t = self._rng.randint(1, 5)
        elif difficulty <= 6:
            n0 = self._rng.randint(100, 500)
            t = self._rng.randint(3, 10)
        else:
            n0 = self._rng.randint(200, 1000)
            t = self._rng.randint(5, 20)

        # Growth factor between 1.2 and 3.0
        factor = round(self._rng.uniform(1.2, 3.0), 2)
        nt = round(n0 * factor)

        r = round(math.log(nt / n0) / t, 4)
        doubling = round(math.log(2) / r, 4) if r > 0 else float("inf")

        problem = f"N_0={n0}, N_t={nt}, t={t}; find r and doubling time"
        return problem, {
            "n0": n0, "nt": nt, "t": t,
            "r": r, "doubling": doubling,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"N_0 = {sd['n0']}, N_t = {sd['nt']}, t = {sd['t']}",
            f"r = ln({sd['nt']}/{sd['n0']}) / {sd['t']} = {sd['r']}",
            f"T_d = ln(2) / {sd['r']} = {sd['doubling']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return growth rate and doubling time.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        return f"r = {sd['r']}; doubling time = {sd['doubling']}"


# ===================================================================
# 8. IMMUNE RESPONSE (tier 4)
# ===================================================================

@register
class ImmuneResponseGenerator(StepGenerator):
    """Compute antibody-antigen binding fraction.

    Equilibrium: K_d = [Ab][Ag] / [AbAg].
    Fraction bound = [Ag] / (K_d + [Ag]).

    Difficulty scaling:
        Difficulty 1-3: K_d and [Ag] as integers.
        Difficulty 4-6: K_d as decimal.
        Difficulty 7-8: multiple antigen concentrations.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "immune_response"

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
        return "compute antibody-antigen binding fraction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an immune response binding problem.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            kd = self._rng.randint(1, 10)
            ag_concs = [self._rng.randint(1, 20)]
        elif difficulty <= 6:
            kd = round(self._rng.uniform(0.5, 10.0), 2)
            ag_concs = [round(self._rng.uniform(1.0, 20.0), 2)]
        else:
            kd = round(self._rng.uniform(0.5, 10.0), 2)
            ag_concs = [round(self._rng.uniform(0.5, 25.0), 2)
                        for _ in range(self._rng.randint(2, 3))]

        fractions: list[float] = []
        steps: list[str] = [f"K_d = {kd}"]
        for ag in ag_concs:
            frac = round(ag / (kd + ag), 4)
            fractions.append(frac)
            steps.append(
                f"[Ag]={ag}: fraction bound = {ag}/({kd}+{ag}) = {frac}"
            )

        problem = f"K_d={kd}; [Ag]={ag_concs}; find fraction bound"
        return problem, {
            "kd": kd, "ag_concs": ag_concs,
            "fractions": fractions, "steps": steps,
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
        """Return the binding fractions.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        pairs = [f"[Ag]={ag}: {f}"
                 for ag, f in zip(sd["ag_concs"], sd["fractions"])]
        return f"fraction bound: {'; '.join(pairs)}"


# ===================================================================
# 9. ALLELE FREQUENCY CHANGE (tier 5)
# ===================================================================

@register
class AlleleFrequencyChangeGenerator(StepGenerator):
    """Compute allele frequency change under selection over generations.

    Iterates p' = p*(p*w_AA + q*w_Aa) / w_bar for 1-3 generations.

    Difficulty scaling:
        Difficulty 1-3: 1 generation.
        Difficulty 4-6: 2 generations.
        Difficulty 7-8: 3 generations.

    Prerequisites:
        multiplication (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "allele_frequency_change"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute allele frequency change over multiple generations"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an allele frequency change problem.

        Args:
            difficulty: Controls number of generations.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            gens = 1
        elif difficulty <= 6:
            gens = 2
        else:
            gens = 3

        p = round(self._rng.uniform(0.2, 0.8), 2)
        w_AA = round(self._rng.uniform(0.8, 1.0), 2)
        w_Aa = round(self._rng.uniform(0.7, 1.0), 2)
        w_aa = round(self._rng.uniform(0.4, 0.9), 2)

        steps: list[str] = [
            f"p_0 = {p}, w_AA={w_AA}, w_Aa={w_Aa}, w_aa={w_aa}"
        ]
        history: list[float] = [p]
        current_p = p

        for gen in range(1, gens + 1):
            q = round(1 - current_p, 4)
            w_bar = round(
                current_p ** 2 * w_AA
                + 2 * current_p * q * w_Aa
                + q ** 2 * w_aa, 4
            )
            numerator = current_p * (current_p * w_AA + q * w_Aa)
            p_new = round(numerator / w_bar, 4) if w_bar > 0 else current_p
            steps.append(
                f"gen {gen}: q={q}, w_bar={w_bar}, p'={p_new}"
            )
            current_p = p_new
            history.append(current_p)

        problem = (f"p={p}, w_AA={w_AA}, w_Aa={w_Aa}, w_aa={w_aa}; "
                   f"{gens} generation(s)")
        return problem, {
            "p_init": p, "w_AA": w_AA, "w_Aa": w_Aa, "w_aa": w_aa,
            "gens": gens, "history": history, "p_final": current_p,
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
        """Return the allele frequency trajectory.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        trajectory = " -> ".join(str(p) for p in sd["history"])
        return f"p: {trajectory}"


# ===================================================================
# 10. GENETIC CODE REDUNDANCY (tier 3)
# ===================================================================

@register
class GeneticCodeRedundancyGenerator(StepGenerator):
    """Count codons encoding each amino acid.

    The standard genetic code has 61 sense codons + 3 stop codons = 64.
    Different amino acids have 1 (Met, Trp) to 6 (Leu, Ser, Arg) codons.

    Difficulty scaling:
        Difficulty 1-3: count codons for 1-2 amino acids.
        Difficulty 4-6: count codons for 3-4 amino acids.
        Difficulty 7-8: count codons for 5-6 amino acids and verify totals.

    Prerequisites:
        division (tier 1).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "genetic_code_redundancy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "count codons encoding each amino acid"

    def _build_aa_counts(self) -> dict[str, int]:
        """Count codons per amino acid from the codon table.

        Returns:
            Dictionary mapping amino acid to codon count.
        """
        counts: dict[str, int] = {}
        for codon, aa in CODON_TABLE.items():
            counts[aa] = counts.get(aa, 0) + 1
        return counts

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a genetic code redundancy problem.

        Args:
            difficulty: Controls number of amino acids queried.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        all_counts = self._build_aa_counts()
        sense_aas = {aa: c for aa, c in all_counts.items() if aa != "Stop"}
        stop_count = all_counts.get("Stop", 3)

        if difficulty <= 3:
            n_query = self._rng.randint(1, 2)
        elif difficulty <= 6:
            n_query = self._rng.randint(3, 4)
        else:
            n_query = self._rng.randint(5, 6)

        aa_list = list(sense_aas.keys())
        self._rng.shuffle(aa_list)
        query_aas = aa_list[:n_query]

        steps: list[str] = []
        results: dict[str, int] = {}
        for aa in query_aas:
            count = sense_aas[aa]
            codons = [c for c, a in CODON_TABLE.items() if a == aa]
            results[aa] = count
            steps.append(f"{aa}: {count} codons ({', '.join(sorted(codons))})")

        total_sense = sum(sense_aas.values())
        steps.append(f"total sense codons: {total_sense}")
        steps.append(f"stop codons: {stop_count}")
        steps.append(f"total: {total_sense + stop_count}")

        degeneracy = round(total_sense / len(sense_aas), 4)
        steps.append(f"avg codons/aa: {degeneracy}")

        aa_desc = ", ".join(query_aas)
        problem = f"count codons for: {aa_desc}"
        return problem, {
            "query_aas": query_aas, "results": results,
            "total_sense": total_sense, "stop_count": stop_count,
            "degeneracy": degeneracy, "steps": steps,
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
        """Return codon counts for queried amino acids.

        Args:
            sd: Solution data.

        Returns:
            Answer string.
        """
        pairs = [f"{aa}={c}" for aa, c in sd["results"].items()]
        return f"codons: {', '.join(pairs)}; avg/aa = {sd['degeneracy']}"
