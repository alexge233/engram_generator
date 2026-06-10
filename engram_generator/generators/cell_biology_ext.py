"""Extended cell biology generators -- signaling, expression, PCR, apoptosis.

6 generators across tiers 4-5 deepening cellular and molecular biology.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class CellBiologyExtBase(StepGenerator):
    """Base class for extended cell biology generators.

    Provides shared constants and template data for signal
    transduction, gene expression, and cell cycle calculations.
    """

    pass


@register
class CellSignalingGenerator(CellBiologyExtBase):
    """Compute signal amplification in a signaling cascade.

    One receptor activates a G-proteins, each activates b effectors.
    Total signal after n steps = a^n * b (final effector output).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cell_signaling"

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
        return "compute signal amplification in a cascade"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a signaling cascade amplification problem.

        Creates cascade parameters: amplification factor per step a,
        final effector multiplier b, and number of steps n. Computes
        total signal = a^n * b.

        Args:
            difficulty: Controls cascade depth and factor sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a = self._rng.randint(2, 5 + difficulty)
        b = self._rng.randint(2, 10 + difficulty)
        n = self._rng.randint(1, min(2 + difficulty // 2, 5))

        a_power_n = a ** n
        total_signal = a_power_n * b
        fold_amplification = total_signal

        desc = (
            f"cascade: a={a} per step, b={b} effectors, "
            f"n={n} steps; find total signal from 1 receptor"
        )
        return desc, {
            "a": a, "b": b, "n": n,
            "a_power_n": a_power_n,
            "total_signal": total_signal,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "total signal = a^n * b",
            f"a^n = {sd['a']}^{sd['n']} = {sd['a_power_n']}",
            f"total = {sd['a_power_n']} * {sd['b']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the total amplified signal.

        Args:
            sd: Solution data.

        Returns:
            Signal magnitude as a string.
        """
        return f"total signal = {sd['total_signal']} molecules"


@register
class GeneExpressionRegulationGenerator(CellBiologyExtBase):
    """Compute fold change and classify gene regulation direction.

    Fold change = expression_condition / expression_control.
    Log2 fold change is computed and classified as up-regulated
    (log2FC >= 1), down-regulated (log2FC <= -1), or unchanged.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gene_expression_regulation"

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
        return "compute fold change and classify gene regulation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gene expression regulation problem.

        Creates control and condition expression values for one or
        more genes, computes fold change and log2 fold change, and
        classifies regulation direction.

        Args:
            difficulty: Controls number of genes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_genes = min(1 + difficulty // 3, 3)
        gene_names = [f"gene_{chr(65 + i)}" for i in range(n_genes)]

        genes_data = []
        for name in gene_names:
            control = round(self._rng.uniform(1.0, 100.0), 4)
            condition = round(self._rng.uniform(0.1, 300.0), 4)
            fc = round(condition / control, 4)
            log2_fc = round(math.log2(fc), 4)

            if log2_fc >= 1:
                regulation = "up-regulated"
            elif log2_fc <= -1:
                regulation = "down-regulated"
            else:
                regulation = "unchanged"

            genes_data.append({
                "name": name, "control": control,
                "condition": condition, "fc": fc,
                "log2_fc": log2_fc, "regulation": regulation,
            })

        desc_parts = [
            f"{g['name']}: ctrl={g['control']}, cond={g['condition']}"
            for g in genes_data
        ]
        desc = "; ".join(desc_parts) + "; classify regulation"

        return desc, {"genes": genes_data}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for g in sd["genes"]:
            steps.append(
                f"{g['name']}: FC = {g['condition']}/{g['control']} = {g['fc']}"
            )
            steps.append(f"log2(FC) = log2({g['fc']}) = {g['log2_fc']}")
            steps.append(f"{g['name']}: {g['regulation']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return classification for all genes.

        Args:
            sd: Solution data.

        Returns:
            Gene regulation classifications.
        """
        parts = [
            f"{g['name']}: log2FC={g['log2_fc']} ({g['regulation']})"
            for g in sd["genes"]
        ]
        return "; ".join(parts)


@register
class CellCycleCheckpointGenerator(CellBiologyExtBase):
    """Identify active cell cycle checkpoint from CDK/cyclin levels.

    Given CDK and cyclin levels at each phase (G1, S, G2, M),
    identifies which checkpoint is active based on level comparison
    against known thresholds.
    """

    CHECKPOINTS = {
        "G1/S (restriction point)": {
            "cyclin_D": "high", "CDK4": "high",
            "cyclin_E": "rising", "CDK2": "rising",
        },
        "intra-S": {
            "cyclin_A": "high", "CDK2": "high",
            "cyclin_E": "falling", "CDK4": "low",
        },
        "G2/M": {
            "cyclin_B": "high", "CDK1": "high",
            "cyclin_A": "falling", "CDK2": "low",
        },
        "spindle assembly (M)": {
            "cyclin_B": "falling", "CDK1": "falling",
            "APC/C": "high", "securin": "degraded",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cell_cycle_checkpoint"

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
        return "identify cell cycle checkpoint from CDK/cyclin levels"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cell cycle checkpoint identification problem.

        Selects a checkpoint and generates its characteristic
        CDK/cyclin profile. At higher difficulty, includes a
        distractor signal.

        Args:
            difficulty: Controls complexity of the profile.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        checkpoint_names = list(self.CHECKPOINTS.keys())
        target = self._rng.choice(checkpoint_names)
        profile = self.CHECKPOINTS[target]

        clues = [f"{k}: {v}" for k, v in profile.items()]

        reasoning = []
        for k, v in profile.items():
            reasoning.append(f"{k} is {v} -> consistent with {target}")

        if difficulty >= 5:
            other = self._rng.choice(
                [c for c in checkpoint_names if c != target]
            )
            other_profile = self.CHECKPOINTS[other]
            distractor_key = self._rng.choice(list(other_profile.keys()))
            clues.append(f"{distractor_key}: {other_profile[distractor_key]} (ambiguous)")
            reasoning.append(f"{distractor_key} signal is from {other} (distractor)")

        clue_str = "; ".join(clues)
        desc = f"observed levels: {clue_str}; identify checkpoint"

        reasoning.append(f"dominant pattern matches {target}")

        return desc, {
            "target": target, "clues": clues,
            "reasoning": reasoning,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["reasoning"]

    def _create_answer(self, sd: dict) -> str:
        """Return the identified checkpoint.

        Args:
            sd: Solution data.

        Returns:
            Checkpoint name string.
        """
        return sd["target"]


@register
class PcrAmplificationGenerator(CellBiologyExtBase):
    """Compute PCR amplification product from initial copies and cycles.

    Standard PCR: copies = initial * 2^n. With efficiency E < 1:
    copies = initial * (1 + E)^n. Computes final copy number.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pcr_amplification"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute PCR amplification product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a PCR amplification problem.

        At lower difficulty, assumes 100% efficiency (copies = N*2^n).
        At higher difficulty, uses a realistic efficiency E < 1.

        Args:
            difficulty: Controls efficiency modeling.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        initial = self._rng.randint(1, 10 * max(1, difficulty))
        n_cycles = self._rng.randint(5, min(15 + difficulty * 3, 35))

        if difficulty <= 4:
            efficiency = 1.0
            copies = initial * (2 ** n_cycles)
            factor = 2 ** n_cycles
            desc = f"initial={initial} copies, {n_cycles} cycles (100% efficiency)"
        else:
            efficiency = round(self._rng.uniform(0.7, 0.95), 4)
            growth = round(1 + efficiency, 4)
            factor = round(growth ** n_cycles, 4)
            copies = round(initial * factor, 4)
            desc = (
                f"initial={initial} copies, {n_cycles} cycles, "
                f"efficiency={efficiency}"
            )

        return desc, {
            "initial": initial, "n_cycles": n_cycles,
            "efficiency": efficiency, "factor": factor,
            "copies": copies,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["efficiency"] == 1.0:
            return [
                f"copies = initial * 2^n",
                f"2^{sd['n_cycles']} = {sd['factor']}",
                f"copies = {sd['initial']} * {sd['factor']}",
            ]
        growth = round(1 + sd["efficiency"], 4)
        return [
            f"copies = initial * (1+E)^n",
            f"1 + E = 1 + {sd['efficiency']} = {growth}",
            f"({growth})^{sd['n_cycles']} = {sd['factor']}",
            f"copies = {sd['initial']} * {sd['factor']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final copy number.

        Args:
            sd: Solution data.

        Returns:
            Copy count as a string.
        """
        return f"{sd['copies']} copies"


@register
class ApoptosisPathwayGenerator(CellBiologyExtBase):
    """Trace apoptosis pathway from triggering signal to caspase activation.

    Given a trigger (death receptor, DNA damage, ER stress), traces
    the signaling pathway to identify intrinsic vs extrinsic apoptosis
    and the key molecular events.
    """

    PATHWAYS = {
        "death_receptor": {
            "type": "extrinsic",
            "steps": [
                "death ligand binds receptor (FasL/Fas or TNF/TNFR)",
                "FADD adaptor recruited to receptor complex",
                "procaspase-8 recruited and activated",
                "caspase-8 activates executioner caspase-3",
            ],
            "trigger": "death receptor ligand binding",
        },
        "DNA_damage": {
            "type": "intrinsic",
            "steps": [
                "DNA damage detected by ATM/ATR kinases",
                "p53 activated and stabilised",
                "pro-apoptotic Bax/Bak activated at mitochondria",
                "cytochrome c released into cytoplasm",
                "apoptosome forms (Apaf-1 + cytochrome c)",
                "caspase-9 activated by apoptosome",
                "caspase-9 activates executioner caspase-3",
            ],
            "trigger": "genotoxic stress (DNA damage)",
        },
        "ER_stress": {
            "type": "intrinsic",
            "steps": [
                "unfolded protein response (UPR) activated",
                "CHOP transcription factor induced",
                "Bcl-2 downregulated, Bax/Bak activated",
                "mitochondrial outer membrane permeabilised",
                "cytochrome c released, apoptosome formed",
                "caspase-9 then caspase-3 activated",
            ],
            "trigger": "ER stress (unfolded proteins)",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "apoptosis_pathway"

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
        return "trace apoptosis pathway and classify intrinsic vs extrinsic"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an apoptosis pathway tracing problem.

        Selects a trigger and generates the pathway description.
        At higher difficulty, asks to compare two pathways.

        Args:
            difficulty: Controls number of pathways.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pathway_keys = list(self.PATHWAYS.keys())
        primary_key = self._rng.choice(pathway_keys)
        primary = self.PATHWAYS[primary_key]

        reasoning = [f"trigger: {primary['trigger']}"]
        for step in primary["steps"][:min(len(primary["steps"]), 3 + difficulty // 2)]:
            reasoning.append(f"-> {step}")
        reasoning.append(f"pathway type: {primary['type']}")

        if difficulty >= 6:
            secondary_key = self._rng.choice(
                [k for k in pathway_keys if k != primary_key]
            )
            secondary = self.PATHWAYS[secondary_key]
            reasoning.append(f"compare: {secondary_key} is {secondary['type']}")
            desc = (
                f"signal: {primary['trigger']}; "
                f"trace pathway and compare with {secondary_key}"
            )
            answer = (
                f"{primary_key}: {primary['type']}, "
                f"{secondary_key}: {secondary['type']}"
            )
        else:
            desc = f"signal: {primary['trigger']}; trace apoptosis pathway"
            answer = f"{primary_key}: {primary['type']} pathway"

        return desc, {
            "primary_key": primary_key,
            "primary_type": primary["type"],
            "reasoning": reasoning,
            "answer": answer,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["reasoning"]

    def _create_answer(self, sd: dict) -> str:
        """Return the pathway classification.

        Args:
            sd: Solution data.

        Returns:
            Pathway type as a string.
        """
        return sd["answer"]


@register
class ReceptorBindingGenerator(CellBiologyExtBase):
    """Compute receptor binding from ligand concentration using saturation kinetics.

    B = Bmax * [L] / (Kd + [L]). Given data points, computes Bmax
    and Kd, or computes B at a given [L] from known parameters.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "receptor_binding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute receptor-ligand binding from saturation kinetics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a receptor binding problem.

        At lower difficulty, gives Bmax, Kd, [L] and asks for B.
        At higher difficulty, gives two data points and asks to
        derive Bmax and Kd.

        Args:
            difficulty: Controls problem mode.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        bmax = round(self._rng.uniform(50.0, 500.0), 4)
        kd = round(self._rng.uniform(0.5, 20.0), 4)

        if difficulty <= 4:
            mode = "find_b"
            lig = round(self._rng.uniform(0.1, 50.0), 4)
            b_val = round(bmax * lig / (kd + lig), 4)
            denom = round(kd + lig, 4)
            numer = round(bmax * lig, 4)

            desc = f"Bmax={bmax}, Kd={kd}, [L]={lig}; find B"
            return desc, {
                "bmax": bmax, "kd": kd, "lig": lig,
                "b_val": b_val, "denom": denom, "numer": numer,
                "mode": mode,
            }

        # Two data points to solve for Bmax and Kd
        mode = "find_params"
        l1 = round(self._rng.uniform(0.5, 10.0), 4)
        l2 = round(self._rng.uniform(15.0, 50.0), 4)
        b1 = round(bmax * l1 / (kd + l1), 4)
        b2 = round(bmax * l2 / (kd + l2), 4)

        # Scatchard: B/[L] = -B/Kd + Bmax/Kd
        # From two points: slope = -1/Kd, intercept = Bmax/Kd
        bl1 = round(b1 / l1, 4)
        bl2 = round(b2 / l2, 4)

        # slope = (bl2 - bl1) / (b2 - b1)
        if abs(b2 - b1) > 1e-10:
            slope = round((bl2 - bl1) / (b2 - b1), 4)
            kd_est = round(-1 / slope, 4) if abs(slope) > 1e-10 else kd
            bmax_est = round(kd_est * bl1 + b1, 4)
        else:
            slope = 0.0
            kd_est = kd
            bmax_est = bmax

        desc = (
            f"[L1]={l1},B1={b1}; [L2]={l2},B2={b2}; "
            f"find Bmax and Kd"
        )
        return desc, {
            "bmax": bmax, "kd": kd,
            "l1": l1, "l2": l2, "b1": b1, "b2": b2,
            "bl1": bl1, "bl2": bl2, "slope": slope,
            "kd_est": kd_est, "bmax_est": bmax_est,
            "mode": mode,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "find_b":
            return [
                "B = Bmax * [L] / (Kd + [L])",
                f"numerator = {sd['bmax']} * {sd['lig']} = {sd['numer']}",
                f"denominator = {sd['kd']} + {sd['lig']} = {sd['denom']}",
                f"B = {sd['numer']} / {sd['denom']}",
            ]
        return [
            "Scatchard: B/[L] = -B/Kd + Bmax/Kd",
            f"B1/[L1] = {sd['b1']}/{sd['l1']} = {sd['bl1']}",
            f"B2/[L2] = {sd['b2']}/{sd['l2']} = {sd['bl2']}",
            f"slope = ({sd['bl2']}-{sd['bl1']})/({sd['b2']}-{sd['b1']}) = {sd['slope']}",
            f"Kd = -1/slope = {sd['kd_est']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed binding or parameters.

        Args:
            sd: Solution data.

        Returns:
            B value or Bmax and Kd.
        """
        if sd["mode"] == "find_b":
            return f"B = {sd['b_val']}"
        return f"Bmax = {sd['bmax_est']}, Kd = {sd['kd_est']}"
