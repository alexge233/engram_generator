"""CLI validation and preview tool for the engram generator curriculum.

Usage:
    engram-validate --task addition --difficulty 5 --samples 100
    engram-validate --tier 2 --samples 50
    engram-validate --all --samples 20
    engram-validate --skill-tree
    engram-validate --stress-test --samples 1000
    engram-validate --preview --task derivative --difficulty 3
    engram-validate --preview --tier 0
"""
import argparse
import sys
import time

from engram_generator.base import STEP_TOKEN
from engram_generator.tokenizer import CharTokenizer
from engram_generator.curriculum.registry import get_all_generators, get_generator


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Validate and preview engram generator curriculum",
    )
    parser.add_argument("--task", type=str, default=None,
                        help="Validate a specific task by name")
    parser.add_argument("--tier", type=int, default=None,
                        help="Validate all tasks in a tier")
    parser.add_argument("--all", action="store_true",
                        help="Validate all tasks")
    parser.add_argument("--skill-tree", action="store_true",
                        help="Print the skill tree structure")
    parser.add_argument("--stress-test", action="store_true",
                        help="Run stress test (many samples per task)")
    parser.add_argument("--preview", action="store_true",
                        help="Rich preview of generated samples with LaTeX")
    parser.add_argument("--samples", type=int, default=50,
                        help="Number of samples to generate per task")
    parser.add_argument("--difficulty", type=int, default=None,
                        help="Override difficulty level")
    parser.add_argument("--max-input", type=int, default=512,
                        help="Maximum input token length")
    parser.add_argument("--max-target", type=int, default=512,
                        help="Maximum target token length")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show sample outputs")
    return parser.parse_args()


def validate_task(task_name: str, num_samples: int, difficulty: int | None,
                  max_input: int, max_target: int, verbose: bool) -> dict:
    """Validate a single task generator.

    Args:
        task_name: Name of the task to validate.
        num_samples: Number of samples to generate.
        difficulty: Override difficulty (None for full range).
        max_input: Maximum input token length.
        max_target: Maximum target token length.
        verbose: Whether to print sample outputs.

    Returns:
        Dict with validation results.
    """
    tokenizer = CharTokenizer()
    gen = get_generator(task_name)

    if difficulty is not None:
        gen.set_difficulty(difficulty, difficulty)

    start = time.time()
    samples = gen.generate(num_samples)
    gen_time = time.time() - start

    results = {
        "task": task_name,
        "tier": gen.tier,
        "generated": len(samples),
        "format_ok": 0,
        "tokens_ok": 0,
        "input_length_ok": 0,
        "target_length_ok": 0,
        "has_steps": 0,
        "has_answer": 0,
        "gen_time_ms": gen_time * 1000,
        "max_input_tokens": 0,
        "max_target_tokens": 0,
        "errors": [],
    }

    for i, sample in enumerate(samples):
        _validate_one_sample(i, sample, tokenizer, max_input, max_target,
                             results, verbose)

    return results


def _check_length(idx: int, label: str, actual: int, limit: int,
                   results: dict, ok_key: str) -> None:
    """Check a token length against a limit and update results.

    Args:
        idx: Sample index.
        label: Field name for error messages.
        actual: Actual token count.
        limit: Maximum allowed.
        results: Results dict to update.
        ok_key: Key to increment on pass.
    """
    if actual <= limit:
        results[ok_key] += 1
    else:
        results["errors"].append(
            f"Sample {idx}: {label} too long ({actual} > {limit})"
        )


def _validate_one_sample(idx: int, sample, tokenizer: CharTokenizer,
                         max_input: int, max_target: int,
                         results: dict, verbose: bool) -> None:
    """Validate a single sample and update results dict.

    Args:
        idx: Sample index.
        sample: The sample to validate.
        tokenizer: Tokenizer for encoding.
        max_input: Max input length.
        max_target: Max target length.
        results: Results dict to update in place.
        verbose: Whether to print sample details.
    """
    input_len = len(tokenizer.encode(sample.input_text))
    target_len = len(tokenizer.encode(sample.target_text))
    results["max_input_tokens"] = max(results["max_input_tokens"], input_len)
    results["max_target_tokens"] = max(results["max_target_tokens"], target_len)

    if STEP_TOKEN in sample.target_text:
        results["format_ok"] += 1
    else:
        results["errors"].append(f"Sample {idx}: missing <step> in target")

    results["tokens_ok"] += 1
    _check_length(idx, "input", input_len, max_input, results, "input_length_ok")
    _check_length(idx, "target", target_len, max_target, results, "target_length_ok")

    if sample.steps:
        results["has_steps"] += 1
    if sample.answer:
        results["has_answer"] += 1

    if verbose and idx < 3:
        print(f"  [{idx}] Input:  {sample.input_text}")
        print(f"      Target: {sample.target_text[:100]}...")
        print(f"      Steps:  {len(sample.steps)}, Answer: {sample.answer}")
        print()


def print_results(results: dict) -> bool:
    """Print validation results and return pass/fail.

    Args:
        results: Dict from validate_task.

    Returns:
        True if all checks passed.
    """
    n = results["generated"]
    passed = (
        results["format_ok"] == n
        and results["tokens_ok"] == n
        and results["input_length_ok"] == n
        and results["target_length_ok"] == n
    )

    status = "PASS" if passed else "FAIL"
    print(f"=== {results['task']} (tier {results['tier']}) === [{status}]")
    print(f"  Generated:     {n} samples in {results['gen_time_ms']:.0f}ms")
    print(f"  Format OK:     {results['format_ok']}/{n}")
    print(f"  Tokens OK:     {results['tokens_ok']}/{n}")
    print(f"  Input OK:      {results['input_length_ok']}/{n} "
          f"(max {results['max_input_tokens']})")
    print(f"  Target OK:     {results['target_length_ok']}/{n} "
          f"(max {results['max_target_tokens']})")
    print(f"  Has steps:     {results['has_steps']}/{n}")
    print(f"  Has answer:    {results['has_answer']}/{n}")

    if results["errors"]:
        print(f"  Errors ({len(results['errors'])}):")
        for err in results["errors"][:5]:
            print(f"    - {err}")
        if len(results["errors"]) > 5:
            print(f"    ... and {len(results['errors']) - 5} more")

    return passed


def _render_sample_panel(console, sample, index: int, total: int,
                         tok: "CharTokenizer", renderer, width: int) -> None:
    """Render a single sample as a rich panel.

    Args:
        console: Rich console instance.
        sample: Sample to render.
        index: Sample index (0-based).
        total: Total number of samples.
        tok: Tokenizer for counting tokens.
        renderer: LatexRenderer instance.
        width: Terminal width.
    """
    from rich.panel import Panel
    from rich.table import Table

    table = Table(show_header=False, box=None, padding=(0, 2), width=width - 4)
    table.add_column("Label", style="bold cyan", width=12)
    table.add_column("Content")

    table.add_row("Input", sample.input_text)
    table.add_row("Problem", renderer.render(sample.problem).strip())
    for j, step in enumerate(sample.steps):
        table.add_row(f"Step {j + 1}", renderer.render(step).strip())
    table.add_row("Answer", f"[bold green]{renderer.render_horizontal(sample.answer).strip()}[/bold green]")
    table.add_row("Tokens", f"in={len(tok.encode(sample.input_text))} out={len(tok.encode(sample.target_text))} d={sample.difficulty}")

    console.print(Panel(table, title=f"Sample {index + 1}/{total}", border_style="dim", width=width))


def preview_task(task_name: str, num_samples: int,
                 difficulty: int | None) -> None:
    """Render samples with rich panels showing input, steps, and answer.

    Args:
        task_name: Task to preview.
        num_samples: Number of samples to show.
        difficulty: Override difficulty (None for full range).
    """
    from rich.console import Console
    from rich.panel import Panel
    from engram_generator.latex_render import LatexRenderer

    console = Console(width=Console().size.width)
    width = console.size.width
    gen = get_generator(task_name)
    tok = CharTokenizer()
    renderer = LatexRenderer()

    if difficulty is not None:
        gen.set_difficulty(difficulty, difficulty)

    console.print()
    console.print(Panel(
        f"[bold]{task_name}[/bold] | Tier {gen.tier} | "
        f"Prerequisites: {', '.join(gen.prerequisites) or 'none'}",
        title="Generator Preview", border_style="blue", width=width,
    ))
    _print_atom_panel(console, task_name, width)

    for i, sample in enumerate(gen.generate(num_samples)):
        _render_sample_panel(console, sample, i, num_samples, tok, renderer, width)


def _print_atom_panel(console, task_name: str,
                      term_width: int = 120) -> None:
    """Print the knowledge atom linked to a task, if available.

    Shows the theorem/definition text, source citation, and URL
    for auditing and verification purposes.

    Args:
        console: Rich console instance.
        task_name: Task name to look up the atom for.
        term_width: Terminal width for panel sizing.
    """
    from rich.panel import Panel
    from rich.text import Text
    from engram_generator.atoms.registry import get_atom

    try:
        atom = get_atom(task_name)
    except KeyError:
        return

    from engram_generator.tokenizer import CharTokenizer
    from engram_generator.latex_render import LatexRenderer

    renderer = LatexRenderer()
    clean = renderer.clean_wikipedia(atom.content)
    rendered_content = renderer.render(clean)

    tok = CharTokenizer()
    token_count = len(tok.encode(clean))

    body = Text()
    body.append(f"Type: ", style="bold")
    body.append(f"{atom.atom_type}\n")
    body.append(f"Domain: ", style="bold")
    body.append(f"{atom.domain}\n")
    body.append(f"Tokens: ", style="bold")
    body.append(f"{token_count}\n\n")
    body.append(rendered_content)
    body.append(f"\n\n")
    body.append(f"Source: ", style="bold cyan")
    body.append(f"{atom.source}\n")
    body.append(f"URL: ", style="bold cyan")
    body.append(f"{atom.source_url}", style="underline")

    console.print(Panel(
        body,
        title=f"Theorem / Definition: {atom.name}",
        border_style="green",
        width=term_width,
    ))


def preview_tier(tier: int, num_samples: int,
                 difficulty: int | None) -> None:
    """Preview all tasks in a tier.

    Args:
        tier: Tier number to preview.
        num_samples: Samples per task.
        difficulty: Override difficulty.
    """
    generators = [g for g in get_all_generators() if g.tier == tier]
    for gen in sorted(generators, key=lambda g: g.task_name):
        preview_task(gen.task_name, num_samples, difficulty)


def main() -> None:
    """CLI entry point."""
    args = parse_args()

    if args.skill_tree:
        _print_skill_tree()
        return

    if args.preview:
        if args.task:
            preview_task(args.task, min(args.samples, 5), args.difficulty)
        elif args.tier is not None:
            preview_tier(args.tier, min(args.samples, 3), args.difficulty)
        else:
            print("--preview requires --task or --tier")
            sys.exit(1)
        return

    generators = []
    if args.task:
        generators = [get_generator(args.task)]
    elif args.tier is not None:
        generators = [g for g in get_all_generators() if g.tier == args.tier]
    elif args.all or args.stress_test:
        generators = get_all_generators()
    else:
        print("Specify --task, --tier, --all, --preview, or --skill-tree")
        sys.exit(1)

    samples = args.samples if not args.stress_test else 1000
    all_passed = True

    for gen in generators:
        results = validate_task(
            gen.task_name, samples, args.difficulty,
            args.max_input, args.max_target, args.verbose,
        )
        passed = print_results(results)
        if not passed:
            all_passed = False
        print()

    print(f"\n{'ALL PASSED' if all_passed else 'SOME FAILED'}")
    sys.exit(0 if all_passed else 1)


def _print_skill_tree() -> None:
    """Print the skill tree as a rich dependency graph."""
    from rich.console import Console
    from rich.tree import Tree

    console = Console()
    generators = get_all_generators()
    by_tier, name_to_tier = _group_by_tier(generators)

    root = Tree("[bold]Engram Curriculum[/bold] (373 tasks)")
    for tier in sorted(by_tier.keys()):
        _add_tier_branch(root, tier, by_tier[tier], name_to_tier)

    console.print(root)
    console.print()


_TIER_LABELS = {
    0: "Basic arithmetic", 1: "Operations", 2: "Intermediate",
    3: "Advanced", 4: "Applied", 5: "Expert", 6: "Graduate",
    7: "Meta-reasoning", 8: "Creative", 9: "Research",
    10: "Self-architecture",
}


def _group_by_tier(generators: list) -> tuple[dict, dict]:
    """Group generators by tier and build a name-to-tier map.

    Args:
        generators: All registered generators.

    Returns:
        Tuple of (by_tier dict, name_to_tier dict).
    """
    by_tier: dict[int, list] = {}
    name_to_tier: dict[str, int] = {}
    for gen in generators:
        by_tier.setdefault(gen.tier, []).append(gen)
        name_to_tier[gen.task_name] = gen.tier
    return by_tier, name_to_tier


def _add_tier_branch(root, tier: int, tier_gens: list,
                     name_to_tier: dict) -> None:
    """Add a tier branch with dependency-nested tasks to the tree.

    Args:
        root: Rich Tree root node.
        tier: Tier number.
        tier_gens: Generators in this tier.
        name_to_tier: Global name-to-tier mapping.
    """
    label = _TIER_LABELS.get(tier, "")
    branch = root.add(
        f"[bold blue]Tier {tier}[/bold blue] -- {label} "
        f"[dim]({len(tier_gens)} tasks)[/dim]"
    )
    tasks = sorted(tier_gens, key=lambda g: g.task_name)
    tier_names = {g.task_name for g in tasks}

    children: dict[str, list] = {}
    roots: list = []
    for gen in tasks:
        same = [p for p in gen.prerequisites if p in tier_names]
        if same:
            children.setdefault(same[0], []).append(gen)
        else:
            roots.append(gen)

    for gen in roots:
        _add_subtree(branch, gen, children, name_to_tier)


def _add_subtree(branch, gen, children: dict, name_to_tier: dict) -> None:
    """Recursively add a task and its same-tier dependents.

    Args:
        branch: Parent tree node.
        gen: Generator to add.
        children: Same-tier dependency map.
        name_to_tier: Global name-to-tier mapping.
    """
    cross = [p for p in gen.prerequisites
             if p in name_to_tier and name_to_tier[p] < gen.tier]
    suffix = f" [dim]<- {', '.join(cross)}[/dim]" if cross else ""
    node = branch.add(f"[green]{gen.task_name}[/green]{suffix}")
    for child in children.get(gen.task_name, []):
        _add_subtree(node, child, children, name_to_tier)
