"""Export validation results to JSONL, CSV, and summary JSON."""
import csv
import json
import os
from pathlib import Path

from engram_generator.validation.result import ValidationReport


class Exporter:
    """Exports validation reports to disk.

    Args:
        report: The validation report to export.
    """

    def __init__(self, report: ValidationReport) -> None:
        """Initialise with a report.

        Args:
            report: Completed validation report.
        """
        self._report = report

    def export_jsonl(self, output_dir: str) -> list[str]:
        """Export one JSONL file per tier.

        Args:
            output_dir: Directory to write files into.

        Returns:
            List of written file paths.
        """
        os.makedirs(output_dir, exist_ok=True)

        by_tier: dict[int, list] = {}
        for r in self._report.results:
            by_tier.setdefault(r.tier, []).append(r)

        paths = []
        for tier in sorted(by_tier.keys()):
            path = os.path.join(output_dir, f"tier_{tier:02d}.jsonl")
            with open(path, "w") as f:
                for result in by_tier[tier]:
                    f.write(json.dumps(result.to_dict()) + "\n")
            paths.append(path)

        return paths

    def export_summary(self, output_path: str) -> str:
        """Export aggregate summary as JSON.

        Args:
            output_path: Path for the summary JSON file.

        Returns:
            The output path.
        """
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        summary = self._report.summary_dict()
        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)
        return output_path

    def export_csv(self, output_path: str) -> str:
        """Export flat CSV with one row per step.

        Args:
            output_path: Path for the CSV file.

        Returns:
            The output path.
        """
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        fieldnames = [
            "generator", "task", "tier", "difficulty", "seed",
            "problem", "step_index", "step_text", "verified",
            "computed", "expected", "answer", "status",
        ]

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in self._report.results:
                if not r.steps:
                    writer.writerow({
                        "generator": r.generator,
                        "task": r.task_name,
                        "tier": r.tier,
                        "difficulty": r.difficulty,
                        "seed": r.seed,
                        "problem": r.problem[:200],
                        "step_index": -1,
                        "step_text": "",
                        "verified": "",
                        "computed": "",
                        "expected": "",
                        "answer": r.answer[:100],
                        "status": r.status,
                    })
                    continue

                for i, step in enumerate(r.steps):
                    writer.writerow({
                        "generator": r.generator,
                        "task": r.task_name,
                        "tier": r.tier,
                        "difficulty": r.difficulty,
                        "seed": r.seed,
                        "problem": r.problem[:200],
                        "step_index": i,
                        "step_text": step.text[:200],
                        "verified": step.verified,
                        "computed": step.computed,
                        "expected": step.expected,
                        "answer": r.answer[:100],
                        "status": r.status,
                    })

        return output_path

    def export_all(self, output_dir: str) -> dict[str, list[str] | str]:
        """Export all formats to a directory.

        Args:
            output_dir: Base output directory.

        Returns:
            Dict with paths: jsonl_files, summary, csv.
        """
        jsonl_dir = os.path.join(output_dir, "jsonl")
        jsonl_files = self.export_jsonl(jsonl_dir)
        summary_path = self.export_summary(
            os.path.join(output_dir, "summary.json"),
        )
        csv_path = self.export_csv(
            os.path.join(output_dir, "validation.csv"),
        )
        return {
            "jsonl_files": jsonl_files,
            "summary": summary_path,
            "csv": csv_path,
        }
