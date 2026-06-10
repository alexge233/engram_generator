#!/usr/bin/env python3
"""Demo script for YouTube video showing Engram Generator in action.

Runs through a curated sequence of generators from basic arithmetic
to self-architecture reasoning, printing samples with colour-coded
output and timing information.

Usage:
    python scripts/demo.py [--speed slow|normal|fast] [--no-color]
"""
import argparse
import math
import sys
import time
from collections import Counter


class ColourPrinter:
    """Handles terminal colour output for the demo."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"

    def __init__(self, enabled: bool = True):
        """Initialise the colour printer.

        Args:
            enabled: Whether to emit ANSI colour codes.
        """
        self._enabled = enabled

    def _c(self, code: str, text: str) -> str:
        """Wrap text in a colour code.

        Args:
            code: ANSI colour code.
            text: Text to colour.

        Returns:
            Colour-wrapped string if enabled, else plain text.
        """
        if not self._enabled:
            return text
        return f"{code}{text}{self.RESET}"

    def bold(self, text: str) -> str:
        """Bold text."""
        return self._c(self.BOLD, text)

    def dim(self, text: str) -> str:
        """Dim text."""
        return self._c(self.DIM, text)

    def cyan(self, text: str) -> str:
        """Cyan text."""
        return self._c(self.CYAN, text)

    def green(self, text: str) -> str:
        """Green text."""
        return self._c(self.GREEN, text)

    def yellow(self, text: str) -> str:
        """Yellow text."""
        return self._c(self.YELLOW, text)

    def magenta(self, text: str) -> str:
        """Magenta text."""
        return self._c(self.MAGENTA, text)

    def red(self, text: str) -> str:
        """Red text."""
        return self._c(self.RED, text)

    def blue(self, text: str) -> str:
        """Blue text."""
        return self._c(self.BLUE, text)


class TypeWriter:
    """Simulates typing text character by character for visual effect."""

    SPEED_MAP = {"slow": 0.03, "normal": 0.012, "fast": 0.003}

    def __init__(self, speed: str = "normal"):
        """Initialise the typewriter.

        Args:
            speed: Typing speed preset ('slow', 'normal', 'fast').
        """
        self._delay = self.SPEED_MAP.get(speed, 0.012)

    def type(self, text: str, instant: bool = False) -> None:
        """Print text with optional typing animation.

        Args:
            text: Text to print.
            instant: If True, print all at once.
        """
        if instant or self._delay <= 0.003:
            print(text)
            return
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(self._delay)
        print()

    def pause(self, seconds: float = 1.0) -> None:
        """Pause for dramatic effect.

        Args:
            seconds: Duration to pause.
        """
        time.sleep(seconds)


class DemoSequence:
    """Curated sequence of generators for the video demo.

    Walks through tiers 0 to 10, showing representative generators
    at increasing complexity. Each entry includes the domain label,
    task name, difficulty, and a one-line description.
    """

    SEQUENCE = [
        # (domain, task_name, difficulty, description)
        ("Basic Arithmetic", "addition", 3, "Add two 3-digit numbers"),
        ("Basic Arithmetic", "multiplication", 2, "Multiply two 2-digit numbers"),
        ("Number Theory", "primality", 3, "Test if a number is prime"),
        ("Number Theory", "gcd", 4, "Greatest common divisor via Euclid"),
        ("Algebra", "quadratic", 3, "Solve a quadratic equation"),
        ("Calculus", "derivative", 4, "Differentiate a polynomial"),
        ("Calculus", "definite_integral", 3, "Evaluate a definite integral"),
        ("Linear Algebra", "matrix_multiply", 3, "Multiply two matrices"),
        ("Linear Algebra", "determinant", 4, "Compute matrix determinant"),
        ("Dynamic Programming", "edit_distance", 3, "Edit distance between strings"),
        ("Graph Algorithms", "dijkstra_trace", 3, "Shortest path via Dijkstra"),
        ("Cryptography", "rsa_encrypt", 4, "RSA encryption"),
        ("Physics", "kinematics_velocity", 3, "Kinematic equations"),
        ("Physics", "lorentz_factor", 3, "Special relativity"),
        ("Quantum Mechanics", "born_rule", 4, "Measurement probabilities"),
        ("Quantum Mechanics", "quantum_gate", 3, "Apply quantum gate"),
        ("Chemistry", "balancing_equation", 3, "Balance chemical equation"),
        ("Thermodynamics", "carnot_efficiency", 3, "Carnot engine efficiency"),
        ("Machine Learning", "backprop_simple", 3, "Backpropagation step"),
        ("Machine Learning", "attention_score", 3, "Attention mechanism"),
        ("Formal Logic", "natural_deduction", 4, "Natural deduction proof"),
        ("Topology", "euler_characteristic", 3, "Euler characteristic"),
        ("Meta-Reasoning", "proof_strategy", 5, "Select proof strategy"),
        ("Meta-Reasoning", "error_taxonomy", 4, "Classify reasoning errors"),
        ("Self-Architecture", "architecture_search", 5, "Search optimal architecture"),
        ("Self-Architecture", "loss_design", 5, "Design a loss function"),
    ]

    def __init__(self):
        """Initialise the demo sequence."""
        self._generators = {}

    def load(self) -> int:
        """Load all generators needed for the demo.

        Returns:
            Number of generators successfully loaded.
        """
        from engram_generator.curriculum.registry import get_generator

        loaded = 0
        for _, task, diff, _ in self.SEQUENCE:
            try:
                gen = get_generator(task, min_difficulty=diff, max_difficulty=diff)
                self._generators[task] = gen
                loaded += 1
            except Exception:
                pass
        return loaded

    def run(self, colour: ColourPrinter, typer: TypeWriter) -> None:
        """Run the full demo sequence.

        Args:
            colour: ColourPrinter for terminal formatting.
            typer: TypeWriter for animated output.
        """
        for i, (domain, task, diff, desc) in enumerate(self.SEQUENCE):
            gen = self._generators.get(task)
            if gen is None:
                continue

            samples = gen.generate(1)
            if not samples:
                continue
            s = samples[0]

            header = f"[{i + 1}/{len(self.SEQUENCE)}] {domain} — Tier {gen.tier}"
            typer.type(colour.bold(colour.cyan(header)))
            typer.type(colour.dim(f"  Task: {task} (difficulty={diff})"))
            typer.type(colour.dim(f"  {desc}"))
            typer.type("")

            typer.type(colour.yellow("  Input:  ") + s.input_text)
            typer.pause(0.3)

            steps = s.target_text.split(" <step> ")
            if len(steps) > 1:
                typer.type(colour.green("  Problem: ") + steps[0])
                for j, step in enumerate(steps[1:-1], 1):
                    typer.type(colour.magenta(f"  Step {j}:  ") + step)
                typer.type(colour.red("  Answer:  ") + colour.bold(steps[-1]))
            else:
                typer.type(colour.green("  Target: ") + s.target_text)

            typer.type("")
            typer.pause(0.8)


class StatsDisplay:
    """Displays generator statistics for the video."""

    def __init__(self, colour: ColourPrinter, typer: TypeWriter):
        """Initialise the stats display.

        Args:
            colour: ColourPrinter instance.
            typer: TypeWriter instance.
        """
        self._colour = colour
        self._typer = typer

    def show_overview(self) -> None:
        """Show high-level statistics about the generator."""
        from engram_generator.curriculum.registry import get_all_generators
        from engram_generator.curriculum.reasoning_patterns import (
            get_pattern_summary,
        )

        c = self._colour
        t = self._typer

        gens = get_all_generators()
        tiers = Counter(g.tier for g in gens)
        patterns = get_pattern_summary(gens)

        t.type(c.bold(c.cyan("=" * 60)))
        t.type(c.bold(c.cyan("  ENGRAM GENERATOR — Overview")))
        t.type(c.bold(c.cyan("=" * 60)))
        t.type("")
        t.type(f"  Total generators:      {c.bold(str(len(gens)))}")
        t.type(f"  Scientific domains:    {c.bold('100+')}")
        t.type(f"  Reasoning patterns:    {c.bold(str(len(patterns)))}")
        t.type(f"  Difficulty levels:     {c.bold('1-8')}")
        t.type(f"  State space:           {c.bold('~10^81 unique problems')}")
        t.type("")

        t.type(c.bold("  Tier Distribution:"))
        for tier in sorted(tiers):
            bar = "█" * (tiers[tier] // 15)
            t.type(f"    Tier {tier:>2}: {tiers[tier]:>4}  {c.green(bar)}")
        t.type("")

    def show_speed_test(self, num_samples: int = 10_000) -> None:
        """Time generation of samples and display throughput.

        Args:
            num_samples: Number of samples to generate for timing.
        """
        from engram_generator.curriculum.registry import get_all_generators

        c = self._colour
        t = self._typer

        gens = get_all_generators()

        t.type(c.bold(c.cyan("  Speed Test")))
        t.type(c.dim(f"  Generating {num_samples:,} samples across all generators..."))
        t.type("")

        start = time.perf_counter()
        total = 0
        per_gen = max(1, num_samples // len(gens))

        for gen in gens:
            samples = gen.generate(per_gen)
            total += len(samples)

        elapsed = time.perf_counter() - start
        rate = total / elapsed

        t.type(f"  Samples generated:  {c.bold(f'{total:,}')}")
        t.type(f"  Time:               {c.bold(f'{elapsed:.2f}s')}")
        t.type(f"  Throughput:         {c.bold(f'{rate:,.0f}')} samples/sec")
        t.type("")

    def show_state_space(self) -> None:
        """Show the state space comparison."""
        c = self._colour
        t = self._typer

        t.type(c.bold(c.cyan("  Why Memorisation is Impossible")))
        t.type("")

        comparisons = [
            ("Google searches (all time)", "10^13"),
            ("Grains of sand on Earth", "10^19"),
            ("Stars in observable universe", "10^24"),
            ("Atoms on Earth", "10^50"),
            ("ENGRAM GENERATOR STATE SPACE", "10^81"),
            ("Atoms in observable universe", "10^80"),
        ]

        for label, power in comparisons:
            if "ENGRAM" in label:
                t.type(f"    {c.bold(c.red(f'{power:>8}'))}  ← {c.bold(label)}")
            else:
                t.type(f"    {c.dim(f'{power:>8}')}    {label}")

        t.type("")
        t.type(c.dim("  Even a 405B model can memorise at most ~10^8 samples."))
        t.type(c.dim("  The gap is 10^73 orders of magnitude."))
        t.type(c.bold("  The only winning strategy is to learn the algorithms."))
        t.type("")

    def show_model_capacity(self) -> None:
        """Show model capacity vs state space analysis."""
        c = self._colour
        t = self._typer

        t.type(c.bold(c.cyan("  Model Capacity Analysis")))
        t.type("")

        bits_per_sample = 300 * math.log2(72)
        models = [
            ("13M (Engram)", 13.2e6),
            ("100M", 100e6),
            ("1B", 1e9),
            ("7B (Llama-2)", 7e9),
            ("70B (Llama-2)", 70e9),
            ("405B (Llama-3)", 405e9),
        ]

        header = f"    {'Model':<20} {'Can Memorise':>14} {'vs 10^81':>12}  Verdict"
        t.type(c.bold(header))
        t.type(c.dim("    " + "-" * 70))

        for name, params in models:
            max_samples = (params * 2) / bits_per_sample
            log_frac = math.log10(max_samples) - 81
            verdict = "MUST REASON"

            if max_samples < 1e5:
                colour_fn = c.red
            elif max_samples < 1e7:
                colour_fn = c.yellow
            else:
                colour_fn = c.yellow

            line = (
                f"    {name:<20} "
                f"{max_samples:>12,.0f}  "
                f"  10^{log_frac:.0f}   "
                f"{colour_fn(verdict)}"
            )
            t.type(line)

        t.type("")
        t.type(c.dim("  Algorithmic info: 1.85 MB. A 1M model has 14x headroom."))
        t.type(c.bold("  Models have enough bits to learn the algorithms,"))
        t.type(c.bold("  but not enough to memorise the instances."))
        t.type("")


class DemoRunner:
    """Orchestrates the full demo for the YouTube video."""

    def __init__(self, speed: str = "normal", use_colour: bool = True):
        """Initialise the demo runner.

        Args:
            speed: Typing speed ('slow', 'normal', 'fast').
            use_colour: Whether to use terminal colours.
        """
        self._colour = ColourPrinter(use_colour)
        self._typer = TypeWriter(speed)
        self._stats = StatsDisplay(self._colour, self._typer)
        self._sequence = DemoSequence()

    def run(self) -> None:
        """Run the complete demo."""
        c = self._colour
        t = self._typer

        # Title card — coloured ASCII logo
        from engram_generator.logo import LOGO_COLOUR, LOGO_PLAIN
        t.type("")
        logo = LOGO_COLOUR if c._enabled else LOGO_PLAIN
        for line in logo.split("\n"):
            t.type(line, instant=True)
        t.type("")
        t.pause(2.0)

        # Part 1: Overview stats
        self._stats.show_overview()
        t.pause(1.5)

        # Part 2: State space
        self._stats.show_state_space()
        t.pause(2.0)

        # Part 3: Model capacity
        self._stats.show_model_capacity()
        t.pause(2.0)

        # Part 4: Live generation
        t.type(c.bold(c.cyan("=" * 60)))
        t.type(c.bold(c.cyan("  Live Generation — Tier 0 to Tier 10")))
        t.type(c.bold(c.cyan("=" * 60)))
        t.type("")

        loaded = self._sequence.load()
        t.type(c.dim(f"  Loaded {loaded} generators. Starting...\n"))
        t.pause(1.0)

        self._sequence.run(c, t)

        # Part 5: Speed test
        t.type(c.bold(c.cyan("=" * 60)))
        self._stats.show_speed_test()

        # Closing
        t.type(c.bold(c.cyan("=" * 60)))
        t.type(c.bold(c.cyan("  The Arc")))
        t.type(c.bold(c.cyan("=" * 60)))
        t.type("")
        t.type("  2 + 3 = 5")
        t.pause(0.5)
        t.type(c.dim("      ↓"))
        t.type("  d/dx(3x^2 + 2x) = 6x + 2")
        t.pause(0.5)
        t.type(c.dim("      ↓"))
        t.type("  curl F = (dFz/dy - dFy/dz, ...)")
        t.pause(0.5)
        t.type(c.dim("      ↓"))
        t.type('  "This proof has an error in step 3."')
        t.pause(0.5)
        t.type(c.dim("      ↓"))
        t.type('  "These two problems share an isomorphic structure."')
        t.pause(0.5)
        t.type(c.dim("      ↓"))
        t.type(c.bold('  "My architecture struggles with length generalisation.'))
        t.type(c.bold('   Here is a proposed modification."'))
        t.type("")
        t.pause(1.0)
        t.type(c.bold("  From following procedures to creating them."))
        t.type(c.bold("  From solving problems to understanding what"))
        t.type(c.bold("  makes problems solvable."))
        t.type("")
        t.type(c.dim("  github.com/alexge233/engram_generator"))
        t.type(c.dim("  www.deepnet.one"))
        t.type("")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Engram Generator demo")
    parser.add_argument(
        "--speed",
        choices=["slow", "normal", "fast"],
        default="normal",
        help="Typing animation speed",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable terminal colours",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    runner = DemoRunner(speed=args.speed, use_colour=not args.no_color)
    runner.run()
