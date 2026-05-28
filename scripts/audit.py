"""Comprehensive audit script for the engram generator codebase.

Runs correctness, structural, code quality, robustness, data quality,
and performance checks across all 373 generators and 387 atoms.
Produces AUDIT_REPORT.md with findings by severity.

Usage:
    python scripts/audit.py --sample-size 20
"""
import argparse
import ast
import hashlib
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engram_generator.base import Sample, StepGenerator, STEP_TOKEN
from engram_generator.tokenizer import CharTokenizer
from engram_generator.curriculum.registry import (
    get_all_generators, get_all_oos_generators, get_prerequisites,
)
from engram_generator.curriculum.skill_tree import SkillTree
from engram_generator.atoms.registry import get_all_atoms, get_atom
from engram_generator.parallel import ParallelGenerator


@dataclass
class Finding:
    """A single audit finding."""
    category: str
    check: str
    severity: str
    message: str
    location: str = ""


class CodeQualityChecker:
    """AST-based static analysis of coding standards."""

    def __init__(self, root: Path):
        self._root = root

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_docstrings())
        findings.extend(self._check_method_size())
        findings.extend(self._check_duplication())
        findings.extend(self._check_dead_code())
        findings.extend(self._check_encapsulation())
        return findings

    def _check_docstrings(self) -> list[Finding]:
        findings = []
        missing = 0
        total = 0
        for py_file in self._root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.startswith("_"):
                        continue
                    total += 1
                    if not (node.body and isinstance(node.body[0], ast.Expr)
                            and isinstance(node.body[0].value, ast.Constant)
                            and isinstance(node.body[0].value.value, str)):
                        missing += 1
        sev = "warning" if missing > 100 else ("info" if missing > 0 else "pass")
        findings.append(Finding("code_quality", "docstrings", sev,
            f"{missing}/{total} public methods missing docstrings"))
        return findings

    def _check_method_size(self) -> list[Finding]:
        findings = []
        large = []
        for py_file in self._root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if hasattr(node, "end_lineno") and node.end_lineno:
                        size = node.end_lineno - node.lineno
                        if size > 50:
                            rel = py_file.relative_to(self._root.parent)
                            large.append((str(rel), node.name, size))
        if large:
            large.sort(key=lambda x: -x[2])
            details = "; ".join(f"{f}:{n} ({s}L)" for f, n, s in large[:10])
            findings.append(Finding("code_quality", "method_size", "warning",
                f"{len(large)} methods exceed 50 lines. Top: {details}"))
        else:
            findings.append(Finding("code_quality", "method_size", "pass",
                "All methods under 50 lines"))
        return findings

    def _check_duplication(self) -> list[Finding]:
        findings = []
        bodies = defaultdict(list)
        for py_file in (self._root / "generators").rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == "_create_answer":
                            h = hashlib.md5(ast.dump(item).encode()).hexdigest()[:8]
                            rel = py_file.relative_to(self._root.parent)
                            bodies[h].append(f"{rel}:{node.name}")
        dupes = {h: c for h, c in bodies.items() if len(c) > 3}
        if dupes:
            total_duped = sum(len(c) for c in dupes.values())
            findings.append(Finding("code_quality", "duplication", "info",
                f"{len(dupes)} groups of duplicated _create_answer ({total_duped} total)"))
        else:
            findings.append(Finding("code_quality", "duplication", "pass",
                "No significant _create_answer duplication"))
        return findings

    def _check_dead_code(self) -> list[Finding]:
        findings = []
        bd = self._root / "base_domains.py"
        if bd.exists():
            text = bd.read_text()
            if "class ScenarioGenerator" in text:
                used = False
                for py_file in self._root.rglob("*.py"):
                    if py_file == bd or "__pycache__" in str(py_file):
                        continue
                    if "ScenarioGenerator" in py_file.read_text():
                        used = True
                        break
                if not used:
                    findings.append(Finding("code_quality", "dead_code", "info",
                        "ScenarioGenerator defined but never subclassed",
                        "engram_generator/base_domains.py"))
        return findings

    def _check_encapsulation(self) -> list[Finding]:
        findings = []
        public_attrs = []
        for py_file in self._root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                            for stmt in ast.walk(item):
                                if (isinstance(stmt, ast.Assign)
                                        and len(stmt.targets) == 1
                                        and isinstance(stmt.targets[0], ast.Attribute)
                                        and isinstance(stmt.targets[0].value, ast.Name)
                                        and stmt.targets[0].value.id == "self"
                                        and not stmt.targets[0].attr.startswith("_")):
                                    rel = py_file.relative_to(self._root.parent)
                                    public_attrs.append(f"{rel}:{node.name}.{stmt.targets[0].attr}")
        if public_attrs:
            sample = ", ".join(public_attrs[:5])
            findings.append(Finding("code_quality", "encapsulation", "info",
                f"{len(public_attrs)} public attributes in __init__: {sample}"))
        else:
            findings.append(Finding("code_quality", "encapsulation", "pass",
                "All instance attributes use underscore prefix"))
        return findings


class StructuralChecker:
    """Verify prerequisite graph, atom coverage, and registry consistency."""

    def __init__(self):
        self._generators = get_all_generators()
        self._names = {g.task_name for g in self._generators}
        self._tier_map = {g.task_name: g.tier for g in self._generators}

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_prereq_graph())
        findings.extend(self._check_atoms())
        findings.extend(self._check_registry())
        return findings

    def _check_prereq_graph(self) -> list[Finding]:
        findings = []
        dangling = [(g.task_name, p) for g in self._generators
                    for p in get_prerequisites(g.task_name) if p not in self._names]
        findings.append(Finding("structural", "dangling_prereqs",
            "fail" if dangling else "pass",
            f"{len(dangling)} dangling prerequisites" + (f": {dangling[:5]}" if dangling else "")))

        backwards = [(g.task_name, p) for g in self._generators
                     for p in g.prerequisites
                     if p in self._tier_map and self._tier_map[p] > g.tier]
        findings.append(Finding("structural", "backwards_prereqs",
            "fail" if backwards else "pass",
            f"{len(backwards)} backwards cross-tier prereqs" + (f": {backwards[:5]}" if backwards else "")))

        # Cycle detection
        adj = defaultdict(list)
        for g in self._generators:
            for p in g.prerequisites:
                if p in self._names:
                    adj[p].append(g.task_name)
        visited, in_stack, has_cycle = set(), set(), [False]
        def dfs(node):
            if node in in_stack: has_cycle[0] = True; return
            if node in visited: return
            visited.add(node); in_stack.add(node)
            for c in adj.get(node, []): dfs(c)
            in_stack.discard(node)
        for n in self._names:
            if n not in visited: dfs(n)
        findings.append(Finding("structural", "cycles",
            "fail" if has_cycle[0] else "pass",
            "Cycle detected" if has_cycle[0] else "No cycles in prerequisite graph"))

        # Reachability
        tier0 = {g.task_name for g in self._generators if g.tier == 0}
        reachable = set(tier0)
        queue = list(tier0)
        while queue:
            node = queue.pop(0)
            for child in adj.get(node, []):
                if child not in reachable:
                    reachable.add(child)
                    queue.append(child)
        unreachable = self._names - reachable
        findings.append(Finding("structural", "reachability",
            "warning" if unreachable else "pass",
            f"{len(unreachable)} unreachable from tier 0" if unreachable
            else f"All {len(self._names)} tasks reachable"))
        return findings

    def _check_atoms(self) -> list[Finding]:
        findings = []
        atoms = get_all_atoms()
        findings.append(Finding("structural", "atom_count",
            "pass" if len(atoms) >= 380 else "warning",
            f"{len(atoms)} atoms registered"))
        bad = [(a.name, f) for a in atoms
               for f in ("name", "content", "domain", "atom_type")
               if not getattr(a, f, None)]
        findings.append(Finding("structural", "atom_fields",
            "warning" if bad else "pass",
            f"{len(bad)} atoms with missing fields" if bad else "All atoms have valid fields"))
        return findings

    def _check_registry(self) -> list[Finding]:
        findings = []
        findings.append(Finding("structural", "registry_size",
            "pass" if len(self._generators) == 373 else "warning",
            f"Registry: {len(self._generators)} generators"))
        oos = get_all_oos_generators()
        findings.append(Finding("structural", "oos_registry",
            "pass" if len(oos) > 0 else "warning",
            f"OOS registry: {len(oos)} generators"))
        return findings


class RobustnessChecker:
    """Verify determinism, exception handling, and parallel safety."""

    def __init__(self, generators: list[StepGenerator]):
        self._generators = generators

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_determinism())
        findings.extend(self._check_exception_handling())
        findings.extend(self._check_parallel_safety())
        return findings

    def _check_determinism(self) -> list[Finding]:
        findings = []
        non_det = []
        for gen in self._generators:
            g1, g2 = type(gen)(seed=42), type(gen)(seed=42)
            s1, s2 = g1.generate(5), g2.generate(5)
            if any(a.target_text != b.target_text for a, b in zip(s1, s2)):
                non_det.append(gen.task_name)
        findings.append(Finding("robustness", "determinism",
            "fail" if non_det else "pass",
            f"{len(non_det)} non-deterministic" if non_det
            else f"All {len(self._generators)} generators deterministic"))
        return findings

    def _check_exception_handling(self) -> list[Finding]:
        findings = []
        root = Path(__file__).resolve().parent.parent / "engram_generator"
        bare, broad = [], []
        for py_file in root.rglob("*.py"):
            if "__pycache__" in str(py_file): continue
            for i, line in enumerate(py_file.read_text().splitlines(), 1):
                s = line.strip()
                if s == "except:":
                    bare.append(f"{py_file.relative_to(root.parent)}:{i}")
                elif "except Exception" in s and "except Exception as" not in s:
                    broad.append(f"{py_file.relative_to(root.parent)}:{i}")
        findings.append(Finding("robustness", "bare_except",
            "fail" if bare else "pass",
            f"{len(bare)} bare except" + (f": {bare}" if bare else "")))
        findings.append(Finding("robustness", "broad_except",
            "info" if broad else "pass",
            f"{len(broad)} broad except Exception" + (f": {broad}" if broad else "")))
        return findings

    def _check_parallel_safety(self) -> list[Finding]:
        findings = []
        from engram_generator.generators.arithmetic_core import AdditionGenerator
        try:
            pg = ParallelGenerator(max_workers=2)
            samples = pg.generate(AdditionGenerator, num_samples=50, base_seed=42)
            ok = len(samples) == 50 and all(s.answer for s in samples)
            findings.append(Finding("robustness", "parallel_safety",
                "pass" if ok else "fail",
                f"ParallelGenerator: {len(samples)}/50 samples"))
        except Exception as e:
            findings.append(Finding("robustness", "parallel_safety", "fail", str(e)))
        return findings


class DataQualityChecker:
    """Verify target lengths, answer formats, LaTeX validity, tokenizer roundtrip."""

    def __init__(self, generators: list[StepGenerator], sample_size: int = 20):
        self._generators = generators
        self._n = sample_size
        self._tok = CharTokenizer()

    def run(self) -> list[Finding]:
        findings = []
        print("  Generating samples for data quality...")
        all_samples = {g.task_name: g.generate(self._n) for g in self._generators}
        findings.extend(self._check_lengths(all_samples))
        findings.extend(self._check_answers(all_samples))
        findings.extend(self._check_braces(all_samples))
        findings.extend(self._check_roundtrip(all_samples))
        return findings

    def _check_lengths(self, samples: dict) -> list[Finding]:
        over256, over512, total, longest = 0, 0, 0, ("", 0)
        for name, ss in samples.items():
            for s in ss:
                total += 1
                ln = len(s.target_text)
                if ln > 256: over256 += 1
                if ln > 512: over512 += 1
                if ln > longest[1]: longest = (name, ln)
        return [Finding("data_quality", "target_lengths", "info",
            f"{over256}/{total} exceed 256 chars, {over512}/{total} exceed 512. "
            f"Longest: {longest[0]} ({longest[1]} chars)")]

    def _check_answers(self, samples: dict) -> list[Finding]:
        findings = []
        bad = [n for n, ss in samples.items() if any(not s.answer or not s.answer.strip() for s in ss)]
        skip = [n for n, ss in samples.items() if any(s.answer == "skip" for s in ss)]
        findings.append(Finding("data_quality", "empty_answers",
            "fail" if bad else "pass",
            f"{len(bad)} generators with empty answers" if bad else "All answers non-empty"))
        findings.append(Finding("data_quality", "skip_answers",
            "warning" if skip else "pass",
            f"{len(skip)} generators fell back to skip" if skip else "No skip fallbacks"))
        return findings

    def _check_braces(self, samples: dict) -> list[Finding]:
        unbal = [n for n, ss in samples.items()
                 if any(s.target_text.count("{") != s.target_text.count("}") for s in ss)]
        return [Finding("data_quality", "latex_braces",
            "warning" if unbal else "pass",
            f"{len(unbal)} with unbalanced braces" if unbal else "All braces balanced")]

    def _check_roundtrip(self, samples: dict) -> list[Finding]:
        vocab = set(self._tok.CHARS)
        missing = {}
        for name, ss in samples.items():
            for s in ss:
                for ch in s.target_text:
                    if ch not in vocab and ch not in "<step>":
                        if ch not in missing: missing[ch] = name
        if missing:
            detail = ", ".join(f"U+{ord(c):04X} in {t}" for c, t in list(missing.items())[:5])
            return [Finding("data_quality", "tokenizer_coverage", "warning",
                f"{len(missing)} chars not in vocab: {detail}")]
        return [Finding("data_quality", "tokenizer_coverage", "pass",
            "All output characters in tokenizer vocabulary")]


class CorrectnessChecker:
    """Verify step-answer consistency and edge cases."""

    def __init__(self, generators: list[StepGenerator], sample_size: int = 20):
        self._generators = generators
        self._n = sample_size

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_step_answer())
        findings.extend(self._check_edge_cases())
        return findings

    def _check_step_answer(self) -> list[Finding]:
        print("  Checking step-answer consistency...")
        mismatches = []
        for gen in self._generators:
            for s in gen.generate(self._n):
                parts = s.target_text.split(f" {STEP_TOKEN} ")
                if parts and parts[-1].strip() != s.answer.strip():
                    mismatches.append(gen.task_name)
                    break
        return [Finding("correctness", "step_answer",
            "fail" if mismatches else "pass",
            f"{len(mismatches)} mismatches" if mismatches
            else f"All {len(self._generators)} generators consistent")]

    def _check_edge_cases(self) -> list[Finding]:
        print("  Checking edge cases...")
        crashes, empties = [], []
        for gen in self._generators:
            for diff in [1, 8]:
                g = type(gen)(min_difficulty=diff, max_difficulty=diff, seed=42)
                try:
                    for s in g.generate(5):
                        if not s.answer or s.answer == "skip":
                            empties.append((gen.task_name, diff))
                            break
                except Exception as e:
                    crashes.append((gen.task_name, diff, str(e)[:50]))
        findings = []
        findings.append(Finding("correctness", "edge_crashes",
            "fail" if crashes else "pass",
            f"{len(crashes)} crash at boundaries" if crashes else "No boundary crashes"))
        findings.append(Finding("correctness", "edge_empty",
            "warning" if empties else "pass",
            f"{len(empties)} skip/empty at boundaries" if empties
            else "No empty answers at boundaries"))
        return findings


class PerformanceChecker:
    """Measure generation speed and skill tree throughput."""

    def __init__(self, generators: list[StepGenerator]):
        self._generators = generators

    def run(self) -> list[Finding]:
        findings = []
        findings.extend(self._check_speed())
        findings.extend(self._check_skill_tree())
        return findings

    def _check_speed(self) -> list[Finding]:
        print("  Profiling generation speed...")
        slow = []
        for gen in self._generators:
            t0 = time.perf_counter()
            gen.generate(100)
            ms = (time.perf_counter() - t0) * 10
            if ms > 100:
                slow.append((gen.task_name, round(ms, 1)))
        if slow:
            slow.sort(key=lambda x: -x[1])
            detail = "; ".join(f"{n} ({m}ms)" for n, m in slow[:5])
            return [Finding("performance", "gen_speed", "warning",
                f"{len(slow)} generators exceed 100ms/sample: {detail}")]
        return [Finding("performance", "gen_speed", "pass",
            f"All {len(self._generators)} under 100ms/sample")]

    def _check_skill_tree(self) -> list[Finding]:
        import random
        tree = SkillTree(self._generators)
        rng = random.Random(42)
        t0 = time.perf_counter()
        for _ in range(100):
            acc = {t: rng.uniform(0.3, 0.99) for t in tree.get_unlocked_tasks()}
            tree.update(acc)
        ms = (time.perf_counter() - t0) * 10
        return [Finding("performance", "skill_tree", "pass" if ms < 100 else "warning",
            f"Skill tree: {ms:.1f}ms/update (100 cycles)")]


class AuditRunner:
    """Orchestrates all checks and produces the report."""

    def __init__(self, sample_size: int = 20, seed: int = 42):
        self._n = sample_size
        self._seed = seed

    def run_all(self) -> list[Finding]:
        findings = []
        root = Path(__file__).resolve().parent.parent / "engram_generator"
        gens = get_all_generators(seed=self._seed)

        print("Phase 1/6: Code quality...")
        findings.extend(CodeQualityChecker(root).run())
        print("Phase 2/6: Structural integrity...")
        findings.extend(StructuralChecker().run())
        print("Phase 3/6: Robustness...")
        findings.extend(RobustnessChecker(gens).run())
        print("Phase 4/6: Data quality...")
        findings.extend(DataQualityChecker(gens, self._n).run())
        print("Phase 5/6: Correctness...")
        findings.extend(CorrectnessChecker(gens, self._n).run())
        print("Phase 6/6: Performance...")
        findings.extend(PerformanceChecker(gens).run())
        return findings

    def write_report(self, findings: list[Finding], path: str) -> None:
        counts = Counter(f.severity for f in findings)
        by_cat = defaultdict(list)
        for f in findings: by_cat[f.category].append(f)

        labels = {"code_quality": "Code Quality", "structural": "Structural Integrity",
                  "robustness": "Robustness", "data_quality": "Data Quality",
                  "correctness": "Correctness", "performance": "Performance"}
        lines = [
            "# Engram Generator Audit Report", "",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Seed: {self._seed} | Samples/generator: {self._n}", "",
            "## Executive Summary", "",
            f"- **Pass**: {counts.get('pass', 0)}",
            f"- **Info**: {counts.get('info', 0)}",
            f"- **Warning**: {counts.get('warning', 0)}",
            f"- **Fail**: {counts.get('fail', 0)}", "",
        ]
        for cat in labels:
            lines.extend([f"## {labels[cat]}", "", "| Check | Status | Details |", "|---|---|---|"])
            for f in by_cat.get(cat, []):
                icon = {"pass": "PASS", "info": "INFO", "warning": "WARN", "fail": "FAIL"}[f.severity]
                msg = f.message.replace("|", "/").replace("\n", " ")
                lines.append(f"| {f.check} | {icon} | {msg} |")
            lines.append("")

        for sev in ("fail", "warning"):
            items = [f for f in findings if f.severity == sev]
            if items:
                lines.extend([f"## {sev.upper()} Details ({len(items)})", ""])
                for f in items:
                    loc = f" ({f.location})" if f.location else ""
                    lines.append(f"- **{f.category}/{f.check}**{loc}: {f.message}")
                lines.append("")

        with open(path, "w") as fh:
            fh.write("\n".join(lines))
        print(f"\nReport: {path}")


def main():
    parser = argparse.ArgumentParser(description="Audit engram generator")
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="AUDIT_REPORT.md")
    args = parser.parse_args()

    runner = AuditRunner(sample_size=args.sample_size, seed=args.seed)
    findings = runner.run_all()
    runner.write_report(findings, args.output)

    counts = Counter(f.severity for f in findings)
    print(f"\nDone: {counts.get('pass',0)} pass, {counts.get('info',0)} info, "
          f"{counts.get('warning',0)} warning, {counts.get('fail',0)} fail")
    sys.exit(1 if counts.get("fail", 0) > 0 else 0)


if __name__ == "__main__":
    main()
