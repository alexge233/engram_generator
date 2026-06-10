"""Cell biology generators -- mitosis, meiosis, transport, ATP, cell cycle.

6 generators across tiers 3-4.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class CellBiologyBase(StepGenerator):
    """Base class for cell biology generators with shared constants.

    Provides common cellular biology constants and template data
    used across mitosis, membrane transport, and metabolic
    generators.
    """

    MITOSIS_PHASES = {
        "prophase": [
            "chromatin condenses into visible chromosomes",
            "nuclear envelope begins to break down",
            "centrioles migrate to opposite poles",
            "spindle fibres begin to form",
        ],
        "metaphase": [
            "chromosomes align at the cell equator",
            "spindle fibres attach to kinetochores",
            "chromosomes are maximally condensed at the metaphase plate",
            "all chromosomes line up along the midline",
        ],
        "anaphase": [
            "sister chromatids separate and move to opposite poles",
            "centromeres split apart",
            "spindle fibres shorten pulling chromatids apart",
            "the cell begins to elongate",
        ],
        "telophase": [
            "nuclear envelopes reform around each set of chromosomes",
            "chromosomes begin to decondense",
            "spindle fibres disassemble",
            "cleavage furrow forms and cytokinesis begins",
        ],
    }

    TRANSPORT_TYPES = {
        "passive diffusion": [
            "small nonpolar molecule moves down its concentration gradient",
            "oxygen crosses the membrane without energy or protein",
            "CO2 passes through the lipid bilayer from high to low concentration",
            "steroid hormone enters cell without a channel or energy",
        ],
        "facilitated diffusion": [
            "glucose enters the cell through a protein channel down its gradient",
            "ions pass through a gated channel without ATP",
            "large polar molecule moves through a carrier protein passively",
            "aquaporin allows water to cross faster than simple diffusion",
        ],
        "active transport": [
            "sodium-potassium pump moves Na+ out and K+ in using ATP",
            "calcium pump moves Ca2+ against its gradient using energy",
            "proton pump uses ATP to move H+ against the concentration gradient",
            "amino acids are transported into the cell against their gradient",
        ],
        "osmosis": [
            "water moves across a semipermeable membrane toward higher solute",
            "net water movement from a hypotonic to a hypertonic solution",
            "water crosses the membrane from dilute to concentrated side",
            "plant cell gains water when placed in a hypotonic solution",
        ],
        "endocytosis": [
            "cell engulfs a large particle by folding the membrane inward",
            "white blood cell surrounds and ingests a bacterium",
            "receptor-mediated uptake of LDL cholesterol via coated pits",
            "pinocytosis brings extracellular fluid into the cell",
        ],
    }

    # ATP yields per molecule for aerobic glucose catabolism
    GLYCOLYSIS_ATP = 2
    PYRUVATE_DECARB_NADH = 2       # 2 NADH -> ~5 ATP
    KREBS_GTP = 2
    KREBS_NADH = 6                  # 6 NADH -> ~15 ATP
    KREBS_FADH2 = 2                 # 2 FADH2 -> ~3 ATP
    NADH_ATP_YIELD = 2.5
    FADH2_ATP_YIELD = 1.5


@register
class MitosisPhaseGenerator(CellBiologyBase):
    """Identify the mitosis phase from a description of cell events.

    Given a template description of cellular events (chromosome
    alignment, spindle formation, etc.), the task is to identify
    which phase of mitosis is being described: prophase, metaphase,
    anaphase, or telophase.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mitosis_phase"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "identify mitosis phase from cell event description"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mitosis phase identification problem.

        Selects a phase and one or more event descriptions from that
        phase. At higher difficulty, includes a distractor event from
        a different phase.

        Args:
            difficulty: Controls number of clues and distractors.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        phases = list(self.MITOSIS_PHASES.keys())
        target_phase = self._rng.choice(phases)
        events = self.MITOSIS_PHASES[target_phase]

        num_clues = min(1 + difficulty // 2, len(events))
        chosen = self._rng.sample(events, num_clues)

        distractor = ""
        if difficulty >= 5:
            other_phases = [p for p in phases if p != target_phase]
            dist_phase = self._rng.choice(other_phases)
            distractor = self._rng.choice(self.MITOSIS_PHASES[dist_phase])
            chosen.append(distractor)
            self._rng.shuffle(chosen)

        clue_text = "; ".join(chosen)

        steps = []
        for clue in chosen:
            if clue == distractor:
                steps.append(f"'{clue}' -> distractor ({dist_phase})")
            else:
                steps.append(f"'{clue}' -> {target_phase}")
        steps.append(f"majority of clues indicate {target_phase}")

        return (
            f"events observed: {clue_text}. Identify the mitosis phase.",
            {
                "target_phase": target_phase,
                "clues": chosen,
                "steps": steps,
            },
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the identified mitosis phase.

        Args:
            sd: Solution data.

        Returns:
            Phase name string.
        """
        return sd["target_phase"]


@register
class MeiosisGametesGenerator(CellBiologyBase):
    """Compute the number of unique gametes from n chromosome pairs.

    The number of unique gamete types from independent assortment
    alone is 2^n where n is the number of homologous chromosome
    pairs. At higher difficulty, crossing over increases variability.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "meiosis_gametes"

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
        return "compute number of unique gametes from chromosome pairs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a meiosis gamete diversity problem.

        At lower difficulty, computes 2^n from independent assortment.
        At higher difficulty, adds a crossing-over factor and asks
        whether the actual diversity exceeds 2^n.

        Args:
            difficulty: Controls chromosome count and crossing over.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(2, min(3 + difficulty, 23))
        base_gametes = 2 ** n

        if difficulty >= 6:
            crossovers = self._rng.randint(1, min(n, difficulty - 3))
            problem = (
                f"organism with {n} chromosome pairs and "
                f"{crossovers} crossover events per meiosis: "
                f"how many unique gamete types?"
            )
            explanation = (
                f"independent assortment gives 2^{n} = {base_gametes}; "
                f"crossing over at {crossovers} sites increases diversity "
                f"beyond {base_gametes}"
            )
            answer_str = f">= {base_gametes} (2^{n} from assortment alone)"
            steps = [
                f"n = {n} chromosome pairs",
                f"independent assortment: 2^{n} = {base_gametes}",
                f"{crossovers} crossover(s) add additional recombinant types",
                explanation,
            ]
        else:
            problem = (
                f"organism with {n} chromosome pairs: "
                f"how many unique gamete types from independent assortment?"
            )
            answer_str = str(base_gametes)
            steps = [
                f"n = {n} chromosome pairs",
                f"unique gametes = 2^n = 2^{n}",
                f"= {base_gametes}",
            ]

        return problem, {
            "n": n,
            "base_gametes": base_gametes,
            "answer": answer_str,
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
        """Return the number of unique gametes.

        Args:
            sd: Solution data.

        Returns:
            Gamete count as string.
        """
        return sd["answer"]


@register
class MembraneTransportGenerator(CellBiologyBase):
    """Classify the type of membrane transport from a description.

    Given a description of how a substance crosses a cell membrane,
    classify it as passive diffusion, facilitated diffusion, active
    transport, osmosis, or endocytosis.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "membrane_transport"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

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
        return "classify membrane transport type from description"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a membrane transport classification problem.

        Selects a transport type and a description from its template
        pool. At higher difficulty, includes a second description to
        compare.

        Args:
            difficulty: Controls number of descriptions.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        types = list(self.TRANSPORT_TYPES.keys())
        target_type = self._rng.choice(types)
        descriptions = self.TRANSPORT_TYPES[target_type]
        desc = self._rng.choice(descriptions)

        steps = [f"observe: '{desc}'"]

        if target_type == "passive diffusion":
            steps.append("no protein, no energy, small nonpolar molecule")
        elif target_type == "facilitated diffusion":
            steps.append("uses protein channel/carrier, no energy, down gradient")
        elif target_type == "active transport":
            steps.append("uses energy (ATP), moves against concentration gradient")
        elif target_type == "osmosis":
            steps.append("water movement across semipermeable membrane")
        else:
            steps.append("membrane folds inward to engulf material")

        steps.append(f"classification: {target_type}")

        if difficulty >= 5:
            other_types = [t for t in types if t != target_type]
            other_type = self._rng.choice(other_types)
            other_desc = self._rng.choice(self.TRANSPORT_TYPES[other_type])
            problem = (
                f"scenario A: {desc} | scenario B: {other_desc}. "
                f"Classify both transport types."
            )
            steps.append(f"scenario B: '{other_desc}' -> {other_type}")
            answer = f"A: {target_type}, B: {other_type}"
        else:
            problem = f"{desc}. Classify the transport type."
            answer = target_type

        return problem, {
            "target_type": target_type,
            "description": desc,
            "answer": answer,
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
        """Return the transport type classification.

        Args:
            sd: Solution data.

        Returns:
            Transport type string.
        """
        return sd["answer"]


@register
class AtpYieldGenerator(CellBiologyBase):
    """Compute total ATP yield from aerobic glucose catabolism.

    Calculates ATP from glycolysis (2 ATP), pyruvate
    decarboxylation (2 NADH = 5 ATP), Krebs cycle (2 GTP +
    6 NADH + 2 FADH2), and oxidative phosphorylation. Total
    is approximately 30-32 ATP per glucose.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "atp_yield"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute total ATP yield from glucose catabolism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ATP yield calculation problem.

        At lower difficulty, computes ATP from a single glucose
        molecule using standard yields. At higher difficulty, scales
        to multiple glucose molecules or asks about specific stages.

        Args:
            difficulty: Controls number of glucose molecules and detail.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        glucose_count = 1
        if difficulty >= 5:
            glucose_count = self._rng.randint(2, min(difficulty, 6))

        # Per-glucose breakdown
        glycolysis_atp = self.GLYCOLYSIS_ATP
        pyr_decarb_nadh_atp = round(
            self.PYRUVATE_DECARB_NADH * self.NADH_ATP_YIELD, 4
        )
        krebs_gtp = self.KREBS_GTP
        krebs_nadh_atp = round(
            self.KREBS_NADH * self.NADH_ATP_YIELD, 4
        )
        krebs_fadh2_atp = round(
            self.KREBS_FADH2 * self.FADH2_ATP_YIELD, 4
        )

        per_glucose = round(
            glycolysis_atp + pyr_decarb_nadh_atp + krebs_gtp
            + krebs_nadh_atp + krebs_fadh2_atp, 4
        )
        total = round(per_glucose * glucose_count, 4)

        if glucose_count == 1:
            problem = "compute total ATP from complete oxidation of 1 glucose"
        else:
            problem = (
                f"compute total ATP from complete oxidation of "
                f"{glucose_count} glucose molecules"
            )

        return problem, {
            "glucose_count": glucose_count,
            "glycolysis_atp": glycolysis_atp,
            "pyr_decarb_nadh_atp": pyr_decarb_nadh_atp,
            "krebs_gtp": krebs_gtp,
            "krebs_nadh_atp": krebs_nadh_atp,
            "krebs_fadh2_atp": krebs_fadh2_atp,
            "per_glucose": per_glucose,
            "total": total,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"glycolysis: {sd['glycolysis_atp']} ATP",
            f"pyruvate decarboxylation: 2 NADH * {self.NADH_ATP_YIELD} = "
            f"{sd['pyr_decarb_nadh_atp']} ATP",
            f"Krebs cycle: {sd['krebs_gtp']} GTP + "
            f"6 NADH * {self.NADH_ATP_YIELD} = {sd['krebs_nadh_atp']} + "
            f"2 FADH2 * {self.FADH2_ATP_YIELD} = {sd['krebs_fadh2_atp']}",
            f"per glucose = {sd['per_glucose']} ATP",
        ]
        if sd["glucose_count"] > 1:
            steps.append(
                f"total = {sd['per_glucose']} * {sd['glucose_count']} = "
                f"{sd['total']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the total ATP yield.

        Args:
            sd: Solution data.

        Returns:
            ATP count string.
        """
        return f"{sd['total']} ATP"


@register
class CellCycleDurationGenerator(CellBiologyBase):
    """Compute cell count after n divisions given a doubling time.

    After n divisions the cell count is 2^n. Given total time and
    doubling time, computes the number of divisions and the final
    cell count.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cell_cycle_duration"

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
        return "compute cell count from doubling time and total time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a cell cycle duration problem.

        Given a doubling time in minutes and a total elapsed time,
        computes the number of complete divisions and final cell
        count. At higher difficulty, starts from multiple initial
        cells.

        Args:
            difficulty: Controls time range and initial cell count.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        doubling_minutes = self._rng.choice([20, 30, 45, 60, 90, 120])
        n_divisions = self._rng.randint(2, min(3 + difficulty, 12))
        total_time = doubling_minutes * n_divisions

        initial_cells = 1
        if difficulty >= 5:
            initial_cells = self._rng.randint(2, min(difficulty * 2, 10))

        cells_per_starter = 2 ** n_divisions
        final_count = initial_cells * cells_per_starter

        if initial_cells == 1:
            problem = (
                f"single cell divides every {doubling_minutes} min for "
                f"{total_time} min: how many cells?"
            )
        else:
            problem = (
                f"{initial_cells} cells each divide every "
                f"{doubling_minutes} min for {total_time} min: "
                f"how many cells?"
            )

        return problem, {
            "doubling_minutes": doubling_minutes,
            "total_time": total_time,
            "n_divisions": n_divisions,
            "initial_cells": initial_cells,
            "cells_per_starter": cells_per_starter,
            "final_count": final_count,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"divisions = {sd['total_time']} / {sd['doubling_minutes']} = "
            f"{sd['n_divisions']}",
            f"cells per starter = 2^{sd['n_divisions']} = "
            f"{sd['cells_per_starter']}",
        ]
        if sd["initial_cells"] > 1:
            steps.append(
                f"total = {sd['initial_cells']} * "
                f"{sd['cells_per_starter']} = {sd['final_count']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final cell count.

        Args:
            sd: Solution data.

        Returns:
            Cell count as string.
        """
        return f"{sd['final_count']} cells"


@register
class OsmolarityGenerator(CellBiologyBase):
    """Compute osmolarity and predict the direction of osmosis.

    Osmolarity = i * M * n where i is the van't Hoff factor
    (number of particles a solute dissociates into), M is molarity,
    and n is the number of solute species. Compares two compartments
    to predict osmotic water flow direction.
    """

    SOLUTES = {
        "NaCl": {"i": 2, "name": "sodium chloride"},
        "KCl": {"i": 2, "name": "potassium chloride"},
        "CaCl2": {"i": 3, "name": "calcium chloride"},
        "glucose": {"i": 1, "name": "glucose"},
        "sucrose": {"i": 1, "name": "sucrose"},
        "MgSO4": {"i": 2, "name": "magnesium sulfate"},
        "Na2SO4": {"i": 3, "name": "sodium sulfate"},
        "urea": {"i": 1, "name": "urea"},
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "osmolarity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute osmolarity and predict direction of osmosis"

    def _compute_osmolarity(self, solute_key: str,
                            molarity: float) -> float:
        """Compute osmolarity for a single solute.

        Args:
            solute_key: Key into SOLUTES dictionary.
            molarity: Molar concentration of the solute.

        Returns:
            Osmolarity value in Osm/L.
        """
        i = self.SOLUTES[solute_key]["i"]
        return round(i * molarity, 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an osmolarity calculation problem.

        Creates two compartments with different solute concentrations.
        Computes osmolarity for each and predicts the direction of
        water movement. At higher difficulty, uses multiple solutes
        per compartment.

        Args:
            difficulty: Controls number of solutes per compartment.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        solute_keys = list(self.SOLUTES.keys())

        # Compartment A
        solute_a = self._rng.choice(solute_keys)
        molarity_a = round(self._rng.uniform(0.05, 0.5), 4)
        osm_a = self._compute_osmolarity(solute_a, molarity_a)

        # Compartment B
        solute_b = self._rng.choice(solute_keys)
        molarity_b = round(self._rng.uniform(0.05, 0.5), 4)
        osm_b = self._compute_osmolarity(solute_b, molarity_b)

        extra_a_osm = 0.0
        extra_b_osm = 0.0
        extra_a_desc = ""
        extra_b_desc = ""

        if difficulty >= 6:
            extra_a_key = self._rng.choice(
                [k for k in solute_keys if k != solute_a]
            )
            extra_a_mol = round(self._rng.uniform(0.01, 0.2), 4)
            extra_a_osm = self._compute_osmolarity(extra_a_key, extra_a_mol)
            osm_a = round(osm_a + extra_a_osm, 4)
            extra_a_desc = f" + {extra_a_mol} M {extra_a_key}"

            extra_b_key = self._rng.choice(
                [k for k in solute_keys if k != solute_b]
            )
            extra_b_mol = round(self._rng.uniform(0.01, 0.2), 4)
            extra_b_osm = self._compute_osmolarity(extra_b_key, extra_b_mol)
            osm_b = round(osm_b + extra_b_osm, 4)
            extra_b_desc = f" + {extra_b_mol} M {extra_b_key}"

        if osm_a > osm_b:
            direction = "water moves from B to A"
            tonicity_a = "hypertonic"
            tonicity_b = "hypotonic"
        elif osm_b > osm_a:
            direction = "water moves from A to B"
            tonicity_a = "hypotonic"
            tonicity_b = "hypertonic"
        else:
            direction = "no net water movement (isotonic)"
            tonicity_a = "isotonic"
            tonicity_b = "isotonic"

        desc_a = f"{molarity_a} M {solute_a}{extra_a_desc}"
        desc_b = f"{molarity_b} M {solute_b}{extra_b_desc}"

        problem = (
            f"compartment A: {desc_a} | "
            f"compartment B: {desc_b}. "
            f"Compute osmolarity and predict osmosis direction."
        )

        i_a = self.SOLUTES[solute_a]["i"]
        i_b = self.SOLUTES[solute_b]["i"]

        steps = [
            f"A: i={i_a}, M={molarity_a}, osmolarity = {i_a}*{molarity_a}"
            f" = {round(i_a * molarity_a, 4)}",
        ]
        if extra_a_osm > 0:
            steps.append(f"A extra solute adds {extra_a_osm} Osm/L")
        steps.append(f"A total osmolarity = {osm_a} Osm/L")
        steps.append(
            f"B: i={i_b}, M={molarity_b}, osmolarity = {i_b}*{molarity_b}"
            f" = {round(i_b * molarity_b, 4)}"
        )
        if extra_b_osm > 0:
            steps.append(f"B extra solute adds {extra_b_osm} Osm/L")
        steps.append(f"B total osmolarity = {osm_b} Osm/L")
        steps.append(f"A is {tonicity_a}, B is {tonicity_b}")

        return problem, {
            "osm_a": osm_a,
            "osm_b": osm_b,
            "direction": direction,
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
        """Return the osmolarity comparison and osmosis direction.

        Args:
            sd: Solution data.

        Returns:
            Answer string with osmolarity values and direction.
        """
        return (
            f"A={sd['osm_a']} Osm/L, B={sd['osm_b']} Osm/L; "
            f"{sd['direction']}"
        )
