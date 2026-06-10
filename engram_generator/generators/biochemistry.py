"""Biochemistry generators -- amino acids, enzymes, DNA, protein structure.

8 generators across tiers 3-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class BiochemistryGenerator(StepGenerator):
    """Base class for biochemistry generators with shared reference data.

    Provides amino acid properties, codon tables, and enzyme kinetics
    constants used across all biochemistry generators.
    """

    AMINO_ACIDS = {
        "Ala": {"abbr": "A", "mass": 89.09, "pKa_NH3": 9.87, "pKa_COOH": 2.35,
                "pKa_side": None, "charge_type": "nonpolar"},
        "Arg": {"abbr": "R", "mass": 174.20, "pKa_NH3": 9.09, "pKa_COOH": 2.18,
                "pKa_side": 12.48, "charge_type": "positive"},
        "Asp": {"abbr": "D", "mass": 133.10, "pKa_NH3": 9.82, "pKa_COOH": 2.09,
                "pKa_side": 3.86, "charge_type": "negative"},
        "Glu": {"abbr": "E", "mass": 147.13, "pKa_NH3": 9.67, "pKa_COOH": 2.10,
                "pKa_side": 4.07, "charge_type": "negative"},
        "Gly": {"abbr": "G", "mass": 75.03, "pKa_NH3": 9.78, "pKa_COOH": 2.35,
                "pKa_side": None, "charge_type": "nonpolar"},
        "His": {"abbr": "H", "mass": 155.16, "pKa_NH3": 9.17, "pKa_COOH": 1.77,
                "pKa_side": 6.10, "charge_type": "positive"},
        "Lys": {"abbr": "K", "mass": 146.19, "pKa_NH3": 9.06, "pKa_COOH": 2.16,
                "pKa_side": 10.54, "charge_type": "positive"},
        "Cys": {"abbr": "C", "mass": 121.16, "pKa_NH3": 10.28, "pKa_COOH": 1.71,
                "pKa_side": 8.33, "charge_type": "polar"},
        "Tyr": {"abbr": "Y", "mass": 181.19, "pKa_NH3": 9.11, "pKa_COOH": 2.20,
                "pKa_side": 10.07, "charge_type": "polar"},
        "Leu": {"abbr": "L", "mass": 131.17, "pKa_NH3": 9.74, "pKa_COOH": 2.33,
                "pKa_side": None, "charge_type": "nonpolar"},
        "Ile": {"abbr": "I", "mass": 131.17, "pKa_NH3": 9.76, "pKa_COOH": 2.32,
                "pKa_side": None, "charge_type": "nonpolar"},
        "Val": {"abbr": "V", "mass": 117.15, "pKa_NH3": 9.72, "pKa_COOH": 2.29,
                "pKa_side": None, "charge_type": "nonpolar"},
        "Phe": {"abbr": "F", "mass": 165.19, "pKa_NH3": 9.31, "pKa_COOH": 2.58,
                "pKa_side": None, "charge_type": "nonpolar"},
        "Ser": {"abbr": "S", "mass": 105.09, "pKa_NH3": 9.21, "pKa_COOH": 2.19,
                "pKa_side": None, "charge_type": "polar"},
        "Thr": {"abbr": "T", "mass": 119.12, "pKa_NH3": 9.10, "pKa_COOH": 2.09,
                "pKa_side": None, "charge_type": "polar"},
    }

    CODON_TABLE = {
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

    AVG_RESIDUE_MASS = 110.0
    WATER_MASS = 18.015


@register
class AminoAcidPropertyGenerator(BiochemistryGenerator):
    """Determine the charge state of an amino acid at a given pH.

    Uses pKa values for the amino group, carboxyl group, and side
    chain (if ionisable) to determine whether the amino acid carries
    a positive, negative, neutral, or zwitterionic charge.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "amino_acid_property"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ph_calculation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "determine amino acid charge state at given pH"

    def _determine_charge(self, aa_data: dict, ph: float) -> tuple[str, list[str]]:
        """Compute net charge and reasoning for an amino acid at a pH.

        Args:
            aa_data: Dictionary with pKa values and charge_type.
            ph: The pH value to evaluate.

        Returns:
            Tuple of (charge_state, reasoning_steps).
        """
        steps = []
        net_charge = 0.0

        # NH3+ group: protonated (positive) when pH < pKa
        pka_nh3 = aa_data["pKa_NH3"]
        if ph < pka_nh3:
            net_charge += 1.0
            steps.append(f"NH3+: pH {ph} < pKa {pka_nh3}, charge +1")
        else:
            steps.append(f"NH2: pH {ph} >= pKa {pka_nh3}, charge 0")

        # COOH group: protonated (neutral) when pH < pKa, deprotonated (-1) when pH > pKa
        pka_cooh = aa_data["pKa_COOH"]
        if ph < pka_cooh:
            steps.append(f"COOH: pH {ph} < pKa {pka_cooh}, charge 0")
        else:
            net_charge -= 1.0
            steps.append(f"COO-: pH {ph} >= pKa {pka_cooh}, charge -1")

        # Side chain
        pka_side = aa_data["pKa_side"]
        if pka_side is not None:
            ct = aa_data["charge_type"]
            if ct == "positive":
                # Side chain protonated = positive
                if ph < pka_side:
                    net_charge += 1.0
                    steps.append(f"side chain: pH {ph} < pKa {pka_side}, charge +1")
                else:
                    steps.append(f"side chain: pH {ph} >= pKa {pka_side}, charge 0")
            elif ct == "negative":
                # Side chain deprotonated = negative
                if ph >= pka_side:
                    net_charge -= 1.0
                    steps.append(f"side chain: pH {ph} >= pKa {pka_side}, charge -1")
                else:
                    steps.append(f"side chain: pH {ph} < pKa {pka_side}, charge 0")
            else:
                # Polar side chains like Cys, Tyr
                if ph >= pka_side:
                    net_charge -= 1.0
                    steps.append(f"side chain: pH {ph} >= pKa {pka_side}, charge -1")
                else:
                    steps.append(f"side chain: pH {ph} < pKa {pka_side}, charge 0")

        net_charge = round(net_charge, 1)

        if net_charge > 0:
            state = "positive"
        elif net_charge < 0:
            state = "negative"
        elif pka_cooh < ph < pka_nh3 and pka_side is None:
            state = "zwitterion"
        else:
            state = "neutral"

        steps.append(f"net charge = {net_charge}")
        return state, steps

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an amino acid charge problem.

        Selects an amino acid and pH value, then determines the
        charge state.

        Args:
            difficulty: Controls which amino acids appear (ionisable
                side chains at higher difficulty).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        aa_names = list(self.AMINO_ACIDS.keys())

        if difficulty <= 3:
            # Only non-ionisable side chains
            candidates = [
                n for n in aa_names if self.AMINO_ACIDS[n]["pKa_side"] is None
            ]
        else:
            candidates = aa_names

        aa_name = self._rng.choice(candidates)
        aa_data = self.AMINO_ACIDS[aa_name]
        ph = round(self._rng.uniform(1.0, 13.0), 1)

        state, reasoning = self._determine_charge(aa_data, ph)

        return (
            f"{aa_name} at pH {ph}: determine charge state",
            {
                "aa_name": aa_name, "ph": ph,
                "state": state, "reasoning": reasoning,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["reasoning"]

    def _create_answer(self, sd: dict) -> str:
        """Return the charge state.

        Args:
            sd: Solution data.

        Returns:
            Charge state string.
        """
        return sd["state"]


@register
class PeptideBondCountGenerator(BiochemistryGenerator):
    """Count peptide bonds in a polypeptide chain.

    A polypeptide with n amino acid residues has exactly n - 1
    peptide bonds connecting them.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "peptide_bond_count"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "count peptide bonds in polypeptide"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a peptide bond counting problem.

        Args:
            difficulty: Controls polypeptide length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(2 + difficulty, 10 + difficulty * 5)
        bonds = n - 1
        return (
            f"polypeptide with {n} amino acids: how many peptide bonds?",
            {"n": n, "bonds": bonds},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "peptide bonds = n - 1",
            f"{sd['n']} - 1 = {sd['bonds']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the peptide bond count.

        Args:
            sd: Solution data.

        Returns:
            Integer count as string.
        """
        return str(sd["bonds"])


@register
class MichaelisMentenGenerator(BiochemistryGenerator):
    """Compute reaction velocity using the Michaelis-Menten equation.

    Uses V = Vmax * [S] / (Km + [S]) to compute reaction velocity
    from substrate concentration, or solves for [S] given V.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "michaelis_menten"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "compute Michaelis-Menten kinetics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Michaelis-Menten kinetics problem.

        At lower difficulty, gives Vmax, Km, [S] and asks for V.
        At higher difficulty, gives V, Vmax, Km and asks for [S].

        Args:
            difficulty: Controls problem mode.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vmax = round(self._rng.uniform(50.0, 500.0), 1)
        km = round(self._rng.uniform(0.5, 20.0), 2)

        if difficulty <= 4:
            s = round(self._rng.uniform(0.1, 50.0), 2)
            v = round(vmax * s / (km + s), 4)
            return (
                f"Vmax={vmax}, Km={km}, [S]={s}: find V",
                {
                    "vmax": vmax, "km": km, "s": s, "v": v,
                    "mode": "find_v",
                },
            )

        # Find [S] given V
        v_frac = round(self._rng.uniform(0.2, 0.8), 2)
        v = round(vmax * v_frac, 2)
        # V = Vmax*S/(Km+S) => S = V*Km/(Vmax-V)
        s = round(v * km / (vmax - v), 4)
        return (
            f"Vmax={vmax}, Km={km}, V={v}: find [S]",
            {
                "vmax": vmax, "km": km, "s": s, "v": v,
                "mode": "find_s",
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "find_v":
            return [
                "V = Vmax * [S] / (Km + [S])",
                f"V = {sd['vmax']} * {sd['s']} / ({sd['km']} + {sd['s']})",
                f"V = {round(sd['vmax'] * sd['s'], 4)} / {round(sd['km'] + sd['s'], 4)}",
            ]
        return [
            "[S] = V * Km / (Vmax - V)",
            f"[S] = {sd['v']} * {sd['km']} / ({sd['vmax']} - {sd['v']})",
            f"[S] = {round(sd['v'] * sd['km'], 4)} / {round(sd['vmax'] - sd['v'], 4)}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed velocity or substrate concentration.

        Args:
            sd: Solution data.

        Returns:
            Answer with appropriate units.
        """
        if sd["mode"] == "find_v":
            return f"V = {sd['v']}"
        return f"[S] = {sd['s']}"


@register
class LineweaverBurkGenerator(BiochemistryGenerator):
    """Determine Km and Vmax from Lineweaver-Burk double reciprocal plot.

    Computes 1/V vs 1/[S] data points from V vs [S] measurements,
    performs linear regression to find slope and intercept, then
    derives Km and Vmax from the y-intercept (1/Vmax) and slope
    (Km/Vmax).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lineweaver_burk"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["linear_regression"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "find Km and Vmax from Lineweaver-Burk plot"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lineweaver-Burk problem.

        Creates V vs [S] data from known Vmax and Km with slight
        noise, then derives the double-reciprocal values.

        Args:
            difficulty: Controls number of data points and noise.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        true_vmax = round(self._rng.uniform(80.0, 300.0), 1)
        true_km = round(self._rng.uniform(1.0, 15.0), 2)
        n_points = min(3 + difficulty, 6)

        s_values = sorted([
            round(self._rng.uniform(0.5, 40.0), 2)
            for _ in range(n_points)
        ])
        v_values = [
            round(true_vmax * s / (true_km + s), 2)
            for s in s_values
        ]

        # Double reciprocal
        inv_s = [round(1.0 / s, 4) for s in s_values]
        inv_v = [round(1.0 / v, 4) for v in v_values]

        # Linear regression on 1/V = (Km/Vmax)(1/S) + 1/Vmax
        n = len(inv_s)
        sum_x = sum(inv_s)
        sum_y = sum(inv_v)
        sum_xy = sum(x * y for x, y in zip(inv_s, inv_v))
        sum_x2 = sum(x ** 2 for x in inv_s)

        denom = n * sum_x2 - sum_x ** 2
        slope = round((n * sum_xy - sum_x * sum_y) / denom, 4)
        intercept = round((sum_y - slope * sum_x) / n, 4)

        # Derive Km and Vmax
        calc_vmax = round(1.0 / intercept, 4) if intercept != 0 else true_vmax
        calc_km = round(slope * calc_vmax, 4)

        data_str = "; ".join(
            f"[S]={s}, V={v}" for s, v in zip(s_values, v_values)
        )
        return (
            f"kinetic data: {data_str}",
            {
                "s_values": s_values, "v_values": v_values,
                "inv_s": inv_s, "inv_v": inv_v,
                "slope": slope, "intercept": intercept,
                "vmax": calc_vmax, "km": calc_km,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        inv_pairs = [
            f"1/{s}={inv_s}" for s, inv_s in zip(sd["s_values"], sd["inv_s"])
        ]
        return [
            f"1/[S] values: {', '.join(inv_pairs[:3])}",
            f"slope = Km/Vmax = {sd['slope']}",
            f"y-intercept = 1/Vmax = {sd['intercept']}",
            f"Vmax = 1/{sd['intercept']} = {sd['vmax']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return Km and Vmax.

        Args:
            sd: Solution data.

        Returns:
            Km and Vmax values.
        """
        return f"Km = {sd['km']}, Vmax = {sd['vmax']}"


@register
class DnaComplementGenerator(BiochemistryGenerator):
    """Write the complementary DNA strand.

    Applies base pairing rules (A-T, G-C) and reverses the
    complement to produce the antiparallel strand (input 5'->3',
    output 3'->5').
    """

    COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dna_complement"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["string_reverse"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "write complementary DNA strand"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DNA complement problem.

        Creates a random DNA sequence and computes its antiparallel
        complement.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        bases = ["A", "T", "G", "C"]
        length = min(4 + difficulty * 2, 20)
        seq = "".join(self._rng.choice(bases) for _ in range(length))
        complement = "".join(self.COMPLEMENT[b] for b in seq)
        antiparallel = complement[::-1]

        return (
            f"5'-{seq}-3': write complementary strand",
            {
                "seq": seq, "complement": complement,
                "antiparallel": antiparallel,
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
            f"pair: A-T, G-C",
            f"complement 5'->3': {sd['complement']}",
            f"reverse for antiparallel: {sd['antiparallel']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the antiparallel complementary strand.

        Args:
            sd: Solution data.

        Returns:
            Complementary strand in 3'->5' notation.
        """
        return f"3'-{sd['antiparallel']}-5'"


@register
class CodonTranslateGenerator(BiochemistryGenerator):
    """Translate an mRNA codon sequence to an amino acid sequence.

    Uses the standard genetic code to translate triplet codons into
    their corresponding amino acids, stopping at a stop codon.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "codon_translate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["dna_complement"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "translate mRNA codons to amino acid sequence"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a codon translation problem.

        Creates a random mRNA sequence starting with AUG (start
        codon) and ending before any internal stop codon.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        num_codons = min(2 + difficulty, 8)
        stop_codons = {"UAA", "UAG", "UGA"}
        rna_bases = ["U", "C", "A", "G"]

        codons = ["AUG"]  # Start codon
        for _ in range(num_codons - 1):
            while True:
                codon = "".join(self._rng.choice(rna_bases) for _ in range(3))
                if codon not in stop_codons:
                    break
            codons.append(codon)

        amino_acids = [self.CODON_TABLE[c] for c in codons]
        mrna = "".join(codons)

        return (
            f"translate mRNA: {mrna}",
            {
                "mrna": mrna, "codons": codons,
                "amino_acids": amino_acids,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for codon, aa in zip(sd["codons"], sd["amino_acids"]):
            steps.append(f"{codon} -> {aa}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the amino acid sequence.

        Args:
            sd: Solution data.

        Returns:
            Hyphen-separated amino acid sequence.
        """
        return "-".join(sd["amino_acids"])


@register
class ProteinMassGenerator(BiochemistryGenerator):
    """Estimate protein molecular weight from amino acid count.

    Uses the average residue mass of approximately 110 Da per amino
    acid, subtracting water lost during peptide bond formation:
    mass = n * 110 - (n - 1) * 18.015.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "protein_mass"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "estimate protein molecular weight"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a protein mass estimation problem.

        At lower difficulty, gives a residue count and asks for
        estimated mass. At higher difficulty, gives a short amino
        acid sequence and uses individual residue masses.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            n = self._rng.randint(10, 50 + difficulty * 30)
            gross = round(n * self.AVG_RESIDUE_MASS, 4)
            water_loss = round((n - 1) * self.WATER_MASS, 4)
            mass = round(gross - water_loss, 4)
            return (
                f"protein with {n} residues: estimate molecular weight",
                {
                    "n": n, "gross": gross,
                    "water_loss": water_loss, "mass": mass,
                    "mode": "estimate",
                },
            )

        # Use individual masses from a short sequence
        aa_names = list(self.AMINO_ACIDS.keys())
        n = self._rng.randint(3, min(6, 2 + difficulty))
        chosen = [self._rng.choice(aa_names) for _ in range(n)]
        individual_masses = [self.AMINO_ACIDS[aa]["mass"] for aa in chosen]
        gross = round(sum(individual_masses), 4)
        water_loss = round((n - 1) * self.WATER_MASS, 4)
        mass = round(gross - water_loss, 4)
        seq_str = "-".join(chosen)
        return (
            f"sequence {seq_str}: compute molecular weight",
            {
                "n": n, "sequence": chosen,
                "individual_masses": individual_masses,
                "gross": gross, "water_loss": water_loss,
                "mass": mass, "mode": "exact",
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "estimate":
            return [
                f"gross = {sd['n']} * {self.AVG_RESIDUE_MASS} = {sd['gross']}",
                f"water loss = ({sd['n']}-1) * {self.WATER_MASS} = {sd['water_loss']}",
                f"mass = {sd['gross']} - {sd['water_loss']}",
            ]
        mass_parts = [
            f"{aa}={m}" for aa, m in zip(sd["sequence"], sd["individual_masses"])
        ]
        return [
            f"residue masses: {', '.join(mass_parts)}",
            f"sum = {sd['gross']}",
            f"water loss = ({sd['n']}-1) * {self.WATER_MASS} = {sd['water_loss']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the molecular weight.

        Args:
            sd: Solution data.

        Returns:
            Mass in Daltons.
        """
        return f"{sd['mass']} Da"


@register
class EnzymeInhibitionGenerator(BiochemistryGenerator):
    """Classify enzyme inhibition type from kinetic data.

    Given Michaelis-Menten kinetic parameters with and without an
    inhibitor, classifies the inhibition as competitive (Km increases,
    Vmax same), uncompetitive (both decrease), or noncompetitive
    (Vmax decreases, Km same).
    """

    INHIBITION_TYPES = ["competitive", "uncompetitive", "noncompetitive"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "enzyme_inhibition"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["michaelis_menten"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description."""
        return "classify enzyme inhibition type from kinetic data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an enzyme inhibition classification problem.

        Creates normal kinetic parameters, picks an inhibition type,
        and modifies Km and/or Vmax accordingly to produce the
        inhibited parameters.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vmax_normal = round(self._rng.uniform(80.0, 300.0), 1)
        km_normal = round(self._rng.uniform(2.0, 15.0), 2)

        inhib_type = self._rng.choice(self.INHIBITION_TYPES)
        factor = round(self._rng.uniform(1.5, 3.0), 1)

        if inhib_type == "competitive":
            km_inhib = round(km_normal * factor, 2)
            vmax_inhib = vmax_normal
            reasoning = "Km increased, Vmax unchanged"
        elif inhib_type == "uncompetitive":
            km_inhib = round(km_normal / factor, 2)
            vmax_inhib = round(vmax_normal / factor, 1)
            reasoning = "both Km and Vmax decreased"
        else:  # noncompetitive
            km_inhib = km_normal
            vmax_inhib = round(vmax_normal / factor, 1)
            reasoning = "Km unchanged, Vmax decreased"

        # Generate V vs [S] data for both conditions
        s_values = sorted([
            round(self._rng.uniform(1.0, 30.0), 1)
            for _ in range(min(3 + difficulty // 2, 5))
        ])
        v_normal = [
            round(vmax_normal * s / (km_normal + s), 2)
            for s in s_values
        ]
        v_inhib = [
            round(vmax_inhib * s / (km_inhib + s), 2)
            for s in s_values
        ]

        normal_str = "; ".join(
            f"[S]={s},V={v}" for s, v in zip(s_values, v_normal)
        )
        inhib_str = "; ".join(
            f"[S]={s},V={v}" for s, v in zip(s_values, v_inhib)
        )

        return (
            f"normal: {normal_str} | inhibited: {inhib_str}",
            {
                "vmax_normal": vmax_normal, "km_normal": km_normal,
                "vmax_inhib": vmax_inhib, "km_inhib": km_inhib,
                "inhib_type": inhib_type, "reasoning": reasoning,
                "factor": factor,
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
            f"normal: Vmax={sd['vmax_normal']}, Km={sd['km_normal']}",
            f"inhibited: Vmax={sd['vmax_inhib']}, Km={sd['km_inhib']}",
            f"compare: {sd['reasoning']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the inhibition type classification.

        Args:
            sd: Solution data.

        Returns:
            Inhibition type with reasoning.
        """
        return f"{sd['inhib_type']} inhibition ({sd['reasoning']})"
