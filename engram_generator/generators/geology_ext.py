"""Extended geology generators -- mineral identification, rock cycle,
stratigraphy, earthquake energy, geologic time, porosity/permeability.

6 generators across tiers 3-5, deepening the geology domain.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. Mineral identification  (tier 3)
# ===================================================================

@register
class MineralIdentificationGenerator(StepGenerator):
    """Identify a mineral from its physical properties.

    Given a set of properties (hardness, luster, streak, cleavage),
    match to one of 10 common minerals using a lookup table.

    Difficulty scaling:
        Difficulty 1-3: provide all four properties, wide separation.
        Difficulty 4-6: provide three properties, must disambiguate.
        Difficulty 7-8: provide two properties; multiple candidates possible.

    Prerequisites:
        comparison.
    """

    _MINERALS: list[dict] = [
        {"name": "quartz", "hardness": 7, "luster": "vitreous",
         "streak": "white", "cleavage": "none (conchoidal fracture)"},
        {"name": "feldspar", "hardness": 6, "luster": "vitreous",
         "streak": "white", "cleavage": "two planes at ~90 degrees"},
        {"name": "mica", "hardness": 2.5, "luster": "pearly",
         "streak": "white", "cleavage": "one perfect plane (sheets)"},
        {"name": "calcite", "hardness": 3, "luster": "vitreous",
         "streak": "white", "cleavage": "three planes (rhombohedral)"},
        {"name": "halite", "hardness": 2.5, "luster": "vitreous",
         "streak": "white", "cleavage": "three planes at 90 degrees (cubic)"},
        {"name": "pyrite", "hardness": 6.5, "luster": "metallic",
         "streak": "greenish-black", "cleavage": "none (conchoidal fracture)"},
        {"name": "magnetite", "hardness": 6, "luster": "metallic",
         "streak": "black", "cleavage": "none (uneven fracture)"},
        {"name": "hematite", "hardness": 5.5, "luster": "metallic",
         "streak": "reddish-brown", "cleavage": "none (uneven fracture)"},
        {"name": "galena", "hardness": 2.5, "luster": "metallic",
         "streak": "lead-gray", "cleavage": "three planes at 90 degrees (cubic)"},
        {"name": "gypsum", "hardness": 2, "luster": "vitreous",
         "streak": "white", "cleavage": "one perfect plane"},
    ]

    _PROPERTIES: list[str] = ["hardness", "luster", "streak", "cleavage"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mineral_identification"

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
        return "identify mineral from physical properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mineral identification problem.

        Selects a mineral and reveals a subset of its properties,
        then asks the student to identify it.

        Args:
            difficulty: Controls how many properties are shown.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mineral = self._rng.choice(self._MINERALS)
        if difficulty <= 3:
            n_props = 4
        elif difficulty <= 6:
            n_props = 3
        else:
            n_props = 2
        shown_keys = self._rng.sample(self._PROPERTIES, n_props)
        clues = [f"{k}={mineral[k]}" for k in shown_keys]
        desc = f"properties: {', '.join(clues)}; identify mineral"
        return desc, {
            "mineral": mineral["name"],
            "clues": clues,
            "shown_keys": shown_keys,
            "mineral_data": {k: mineral[k] for k in shown_keys},
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"observed: {c}" for c in sd["clues"]]
        steps.append(f"match lookup table -> {sd['mineral']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the identified mineral.

        Args:
            sd: Solution data.

        Returns:
            Mineral name.
        """
        return sd["mineral"]


# ===================================================================
# 2. Rock cycle  (tier 3)
# ===================================================================

@register
class RockCycleGenerator(StepGenerator):
    """Determine resulting rock type from a starting rock and process.

    Given a starting rock type (igneous, sedimentary, metamorphic) and
    a geological process (melting+cooling, weathering+deposition+
    lithification, heat+pressure), determine the resulting rock type.

    Difficulty scaling:
        Difficulty 1-3: single process transformation.
        Difficulty 4-6: chain of two processes.
        Difficulty 7-8: chain of three processes.

    Prerequisites:
        comparison.
    """

    _TRANSITIONS: dict[tuple[str, str], str] = {
        ("igneous", "weathering"): "sedimentary",
        ("igneous", "heat+pressure"): "metamorphic",
        ("igneous", "melting+cooling"): "igneous",
        ("sedimentary", "weathering"): "sedimentary",
        ("sedimentary", "heat+pressure"): "metamorphic",
        ("sedimentary", "melting+cooling"): "igneous",
        ("metamorphic", "weathering"): "sedimentary",
        ("metamorphic", "heat+pressure"): "metamorphic",
        ("metamorphic", "melting+cooling"): "igneous",
    }

    _ROCK_TYPES: list[str] = ["igneous", "sedimentary", "metamorphic"]
    _PROCESSES: list[str] = ["weathering", "heat+pressure", "melting+cooling"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rock_cycle"

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
        return "determine rock type after geological process"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rock cycle transformation problem.

        Creates a chain of geological processes and tracks the
        resulting rock type through each step.

        Args:
            difficulty: Controls the length of the process chain.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_steps = 1
        elif difficulty <= 6:
            n_steps = 2
        else:
            n_steps = 3

        start = self._rng.choice(self._ROCK_TYPES)
        processes: list[str] = []
        intermediates: list[str] = [start]
        current = start
        for _ in range(n_steps):
            proc = self._rng.choice(self._PROCESSES)
            processes.append(proc)
            current = self._TRANSITIONS[(current, proc)]
            intermediates.append(current)

        chain_str = " -> ".join(processes)
        desc = f"start: {start}, processes: {chain_str}; result?"
        return desc, {
            "start": start,
            "processes": processes,
            "intermediates": intermediates,
            "result": current,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for i, proc in enumerate(sd["processes"]):
            steps.append(
                f"{sd['intermediates'][i]} + {proc} -> "
                f"{sd['intermediates'][i + 1]}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the resulting rock type.

        Args:
            sd: Solution data.

        Returns:
            Final rock type.
        """
        return sd["result"]


# ===================================================================
# 3. Stratigraphy  (tier 4)
# ===================================================================

@register
class StratigraphyGenerator(StepGenerator):
    """Order geological events using superposition and cross-cutting.

    Applies the law of superposition (oldest at bottom) and the
    principle of cross-cutting relationships (intrusion younger than
    cut layers) to order 4-6 geological events.

    Difficulty scaling:
        Difficulty 1-3: 4 layers, no cross-cutting.
        Difficulty 4-6: 5 layers with one cross-cutting intrusion.
        Difficulty 7-8: 6 layers with two cross-cutting intrusions.

    Prerequisites:
        comparison.
    """

    _LAYER_NAMES: list[str] = [
        "sandstone", "limestone", "shale", "mudstone",
        "conglomerate", "chalk", "dolomite", "siltstone",
    ]
    _INTRUSION_NAMES: list[str] = ["granite intrusion", "basalt dike"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stratigraphy"

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
        return "order geological events by superposition and cross-cutting"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stratigraphy ordering problem.

        Builds a stratigraphic column with optional cross-cutting
        intrusions and asks for chronological ordering.

        Args:
            difficulty: Controls number of layers and intrusions.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_layers = 4
            n_intrusions = 0
        elif difficulty <= 6:
            n_layers = 4
            n_intrusions = 1
        else:
            n_layers = 4
            n_intrusions = 2

        layers = self._rng.sample(self._LAYER_NAMES, n_layers)
        # Layers listed bottom to top (oldest first)
        # Chronological age: index 0 = oldest
        order: list[str] = list(layers)  # oldest to youngest

        intrusions_desc: list[str] = []
        for i in range(n_intrusions):
            intr_name = self._INTRUSION_NAMES[i % len(self._INTRUSION_NAMES)]
            cut_idx = self._rng.randint(0, len(layers) - 1)
            intrusions_desc.append(
                f"{intr_name} cuts through {layers[cut_idx]}"
            )
            # Intrusion is younger than the layer it cuts
            order.append(intr_name)

        # Present layers from top to bottom (youngest first for confusion)
        display = list(reversed(layers))
        display_str = " (top) | ".join(display) + " (bottom)"

        intr_str = ""
        if intrusions_desc:
            intr_str = "; " + "; ".join(intrusions_desc)

        desc = f"column top-to-bottom: {display_str}{intr_str}; order oldest to youngest"
        return desc, {
            "layers": layers,
            "order": order,
            "intrusions_desc": intrusions_desc,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["law of superposition: bottom layers are older"]
        for i, layer in enumerate(sd["layers"]):
            steps.append(f"position {i + 1} (bottom-up): {layer}")
        for intr in sd["intrusions_desc"]:
            steps.append(f"cross-cutting: {intr} -> intrusion is younger")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the chronological order.

        Args:
            sd: Solution data.

        Returns:
            Oldest-to-youngest ordering.
        """
        return " -> ".join(sd["order"])


# ===================================================================
# 4. Earthquake energy  (tier 5)
# ===================================================================

@register
class EarthquakeEnergyGenerator(StepGenerator):
    """Compute seismic energy from magnitude and compare earthquakes.

    Uses log10(E) = 1.5*M + 4.8 (energy in Joules). Given one or
    two magnitudes, compute energy and optionally the energy ratio
    between two earthquakes.

    Difficulty scaling:
        Difficulty 1-3: compute energy for one earthquake.
        Difficulty 4-6: compute energy for two and find ratio.
        Difficulty 7-8: given energy, find magnitude (inverse).

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "earthquake_energy"

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
        return "compute earthquake energy from magnitude"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an earthquake energy problem.

        At lower difficulties, computes energy from one magnitude.
        At higher difficulties, compares two earthquakes or inverts.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            m = round(self._rng.uniform(2.0, 7.0), 1)
            log_e = round(1.5 * m + 4.8, 4)
            energy = round(10.0 ** log_e, 4)
            desc = f"magnitude M = {m}; compute energy (Joules)"
            return desc, {
                "mode": "single", "m": m, "log_e": log_e, "energy": energy,
            }
        elif difficulty <= 6:
            m1 = round(self._rng.uniform(3.0, 7.0), 1)
            m2 = round(self._rng.uniform(3.0, 7.0), 1)
            while m1 == m2:
                m2 = round(self._rng.uniform(3.0, 7.0), 1)
            log_e1 = round(1.5 * m1 + 4.8, 4)
            log_e2 = round(1.5 * m2 + 4.8, 4)
            ratio = round(10.0 ** (log_e1 - log_e2), 4)
            desc = f"M1 = {m1}, M2 = {m2}; energy ratio E1/E2?"
            return desc, {
                "mode": "ratio", "m1": m1, "m2": m2,
                "log_e1": log_e1, "log_e2": log_e2, "ratio": ratio,
            }
        else:
            log_e = round(self._rng.uniform(8.0, 16.0), 2)
            m = round((log_e - 4.8) / 1.5, 4)
            desc = f"log10(E) = {log_e}; find magnitude M"
            return desc, {
                "mode": "inverse", "log_e": log_e, "m": m,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "single":
            return [
                "log10(E) = 1.5*M + 4.8",
                f"log10(E) = 1.5*{sd['m']} + 4.8 = {sd['log_e']}",
                f"E = 10^{sd['log_e']} = {sd['energy']} J",
            ]
        elif sd["mode"] == "ratio":
            diff = round(sd["log_e1"] - sd["log_e2"], 4)
            return [
                "log10(E) = 1.5*M + 4.8",
                f"log10(E1) = {sd['log_e1']}, log10(E2) = {sd['log_e2']}",
                f"log10(E1/E2) = {sd['log_e1']} - {sd['log_e2']} = {diff}",
                f"E1/E2 = 10^{diff} = {sd['ratio']}",
            ]
        else:
            return [
                "M = (log10(E) - 4.8) / 1.5",
                f"M = ({sd['log_e']} - 4.8) / 1.5 = {sd['m']}",
            ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed energy or magnitude.

        Args:
            sd: Solution data.

        Returns:
            Result as a string.
        """
        if sd["mode"] == "single":
            return f"E = {sd['energy']} J"
        elif sd["mode"] == "ratio":
            return f"E1/E2 = {sd['ratio']}"
        else:
            return f"M = {sd['m']}"


# ===================================================================
# 5. Geologic time  (tier 4)
# ===================================================================

@register
class GeologicTimeGenerator(StepGenerator):
    """Place geological events in chronological order and compute spans.

    Given absolute dates (in Ma) and period names, place events in
    chronological order and compute the time span between two events.

    Difficulty scaling:
        Difficulty 1-3: 3 events, simple ordering.
        Difficulty 4-6: 4 events, compute one time span.
        Difficulty 7-8: 5 events, compute two time spans.

    Prerequisites:
        subtraction.
    """

    _EVENTS: list[dict] = [
        {"name": "formation of Earth", "date_ma": 4540},
        {"name": "Great Oxidation Event", "date_ma": 2400},
        {"name": "Cambrian explosion", "date_ma": 541},
        {"name": "first land plants", "date_ma": 470},
        {"name": "Permian-Triassic extinction", "date_ma": 252},
        {"name": "first dinosaurs", "date_ma": 230},
        {"name": "K-Pg extinction", "date_ma": 66},
        {"name": "first Homo sapiens", "date_ma": 0.3},
        {"name": "end of last ice age", "date_ma": 0.012},
        {"name": "Carboniferous period start", "date_ma": 359},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "geologic_time"

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
        return "order geological events and compute time spans"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a geologic time ordering problem.

        Selects events and asks for chronological ordering plus
        time span computation between selected pairs.

        Args:
            difficulty: Controls number of events and spans.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_events = 3
            n_spans = 0
        elif difficulty <= 6:
            n_events = 4
            n_spans = 1
        else:
            n_events = 5
            n_spans = 2

        chosen = self._rng.sample(self._EVENTS, n_events)
        # Shuffle for presentation
        shuffled = list(chosen)
        self._rng.shuffle(shuffled)
        # Sort by date (oldest first = largest Ma)
        ordered = sorted(chosen, key=lambda e: -e["date_ma"])

        spans: list[dict] = []
        if n_spans >= 1 and len(ordered) >= 2:
            i, j = 0, 1
            span_val = round(ordered[i]["date_ma"] - ordered[j]["date_ma"], 4)
            spans.append({
                "from": ordered[i]["name"], "to": ordered[j]["name"],
                "span": span_val,
            })
        if n_spans >= 2 and len(ordered) >= 4:
            i, j = 2, 3
            span_val = round(ordered[i]["date_ma"] - ordered[j]["date_ma"], 4)
            spans.append({
                "from": ordered[i]["name"], "to": ordered[j]["name"],
                "span": span_val,
            })

        events_str = "; ".join(
            f"{e['name']} ({e['date_ma']} Ma)" for e in shuffled
        )
        desc = f"events: {events_str}; order oldest to youngest"
        if spans:
            desc += "; compute time spans between consecutive pairs"

        return desc, {
            "shuffled": shuffled,
            "ordered": ordered,
            "spans": spans,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["larger Ma = older event"]
        for i, e in enumerate(sd["ordered"]):
            steps.append(f"{i + 1}. {e['name']} ({e['date_ma']} Ma)")
        for sp in sd["spans"]:
            steps.append(
                f"span: {sp['from']} to {sp['to']} = {sp['span']} Ma"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the chronological order and spans.

        Args:
            sd: Solution data.

        Returns:
            Ordered events with optional spans.
        """
        order_str = " -> ".join(e["name"] for e in sd["ordered"])
        if sd["spans"]:
            span_strs = [f"{s['span']} Ma" for s in sd["spans"]]
            return f"{order_str}; spans: {', '.join(span_strs)}"
        return order_str


# ===================================================================
# 6. Porosity and permeability (Darcy's law)  (tier 4)
# ===================================================================

@register
class PorosityPermeabilityGenerator(StepGenerator):
    """Compute porosity and flow rate via Darcy's law.

    Porosity = V_pore / V_total. Darcy's law for flow rate:
    Q = k * A * (dP / dx) / mu, where k is permeability, A is
    cross-sectional area, dP/dx is pressure gradient, and mu is
    dynamic viscosity.

    Difficulty scaling:
        Difficulty 1-3: compute porosity only.
        Difficulty 4-6: compute Q from Darcy's law with given params.
        Difficulty 7-8: compute both porosity and flow rate.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "porosity_permeability"

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
        return "compute porosity and/or Darcy flow rate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a porosity/permeability problem.

        At lower difficulties, computes porosity from pore and total
        volumes. At higher difficulties, applies Darcy's law.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            v_total = round(self._rng.uniform(50.0, 200.0), 1)
            porosity_frac = round(self._rng.uniform(0.05, 0.45), 2)
            v_pore = round(v_total * porosity_frac, 4)
            porosity = round(v_pore / v_total, 4)
            desc = (
                f"V_pore = {v_pore} cm^3, V_total = {v_total} cm^3; "
                f"compute porosity"
            )
            return desc, {
                "mode": "porosity",
                "v_pore": v_pore, "v_total": v_total,
                "porosity": porosity,
            }
        else:
            # Darcy's law: Q = k * A * (dP/dx) / mu
            # k in millidarcys, convert: 1 mD = 9.869e-16 m^2
            k_md = round(self._rng.uniform(10.0, 500.0), 1)
            k_m2 = round(k_md * 9.869e-16, 4)
            area = round(self._rng.uniform(0.01, 1.0), 4)  # m^2
            dp = round(self._rng.uniform(1e4, 1e6), 0)  # Pa
            dx = round(self._rng.uniform(1.0, 100.0), 1)  # m
            mu = round(self._rng.uniform(0.001, 0.01), 4)  # Pa*s
            dp_dx = round(dp / dx, 4)
            q = round(k_m2 * area * dp_dx / mu, 4)

            desc = (
                f"k = {k_md} mD, A = {area} m^2, dP = {dp} Pa, "
                f"dx = {dx} m, mu = {mu} Pa*s; Darcy flow rate Q?"
            )
            return desc, {
                "mode": "darcy",
                "k_md": k_md, "k_m2": k_m2, "area": area,
                "dp": dp, "dx": dx, "mu": mu,
                "dp_dx": dp_dx, "q": q,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "porosity":
            return [
                "porosity = V_pore / V_total",
                f"porosity = {sd['v_pore']} / {sd['v_total']} = {sd['porosity']}",
            ]
        return [
            "Q = k * A * (dP/dx) / mu",
            f"k = {sd['k_md']} mD = {sd['k_m2']} m^2",
            f"dP/dx = {sd['dp']} / {sd['dx']} = {sd['dp_dx']} Pa/m",
            f"Q = {sd['k_m2']} * {sd['area']} * {sd['dp_dx']} / {sd['mu']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed porosity or flow rate.

        Args:
            sd: Solution data.

        Returns:
            Result as a string.
        """
        if sd["mode"] == "porosity":
            return f"porosity = {sd['porosity']}"
        return f"Q = {sd['q']} m^3/s"
