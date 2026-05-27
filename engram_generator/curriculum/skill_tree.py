"""Adaptive skill tree for curriculum management."""
from dataclasses import dataclass, field

from engram_generator.base import StepGenerator


@dataclass
class SkillNode:
    """A task node in the skill tree.

    Attributes:
        task_name: Generator name.
        tier: Skill tier (0-10).
        prerequisites: Task names that must be mastered first.
        current_difficulty: Current difficulty level.
        max_difficulty: Maximum difficulty the generator supports.
        accuracy_history: Per-epoch accuracy for tracking.
        unlocked: Whether this task is active in training.
        mastered: Whether this task has been mastered (accuracy > mastery_threshold).
        mastery_threshold: Accuracy needed to consider mastered.
        escalation_threshold: Accuracy to trigger difficulty increase.
    """

    task_name: str
    tier: int = 0
    prerequisites: list[str] = field(default_factory=list)
    current_difficulty: int = 1
    max_difficulty: int = 8
    accuracy_history: list[float] = field(default_factory=list)
    unlocked: bool = False
    mastered: bool = False
    mastery_threshold: float = 0.90
    escalation_threshold: float = 0.95


class SkillTree:
    """Manages the adaptive curriculum — tracks mastery and unlocks tasks.

    The skill tree:
    1. Starts with Tier 0 tasks unlocked
    2. Each epoch, checks per-task accuracy
    3. Escalates difficulty when a task hits escalation_threshold
    4. Unlocks new tasks when all prerequisites are mastered
    5. Tracks mastery state for sampling weight decisions

    Attributes:
        nodes: Dict of task_name → SkillNode.
        retention_ratio: Fraction of samples from mastered tasks (0.0 to disable).
    """

    def __init__(self, generators: list[StepGenerator],
                 retention_ratio: float = 0.1):
        """Build the skill tree from a list of generators.

        Args:
            generators: All available task generators.
            retention_ratio: Fraction of training samples for mastered tasks.
        """
        self._nodes: dict[str, SkillNode] = {}
        self._retention_ratio = retention_ratio

        for gen in generators:
            self._nodes[gen.task_name] = SkillNode(
                task_name=gen.task_name,
                tier=gen.tier,
                prerequisites=gen.prerequisites,
                max_difficulty=gen.max_difficulty,
            )

        self._unlock_tier(0)

    def _unlock_tier(self, tier: int) -> None:
        """Unlock all tasks at the given tier with no prerequisites.

        Args:
            tier: Tier to unlock.
        """
        for node in self._nodes.values():
            if node.tier == tier and not node.prerequisites:
                node.unlocked = True

    def update(self, accuracy_per_task: dict[str, float]) -> dict[str, str]:
        """Update skill tree state based on validation accuracy.

        Processes accuracy for all unlocked tasks, then propagates
        unlocks from newly mastered prerequisites. Repeats until no
        more tasks unlock, handling same-tier prerequisite chains
        (e.g. multiplication T1 -> area_rectangle T1 -> area_triangle T1).

        Args:
            accuracy_per_task: Dict of task_name to accuracy from last epoch.

        Returns:
            Dict of events that occurred (for logging):
            task_name to event string ("escalated", "mastered", "unlocked").
        """
        events: dict[str, str] = {}

        self._apply_accuracy(accuracy_per_task, events)

        while True:
            newly_unlocked = self._check_unlocks()
            if not newly_unlocked:
                break
            for task_name in newly_unlocked:
                events[task_name] = "unlocked"
            pending = {n: accuracy_per_task[n] for n in newly_unlocked
                       if n in accuracy_per_task}
            if not pending:
                break
            self._apply_accuracy(pending, events)

        return events

    def _apply_accuracy(self, accuracy_per_task: dict[str, float],
                        events: dict[str, str]) -> None:
        """Process accuracy updates for unlocked tasks.

        Escalates difficulty and marks mastery where thresholds are met.
        Only processes tasks that are currently unlocked.

        Args:
            accuracy_per_task: Dict of task_name to accuracy.
            events: Events dict to update in place.
        """
        for task_name, accuracy in accuracy_per_task.items():
            if task_name not in self._nodes:
                continue

            node = self._nodes[task_name]
            if accuracy not in [h for h in node.accuracy_history[-1:]]:
                node.accuracy_history.append(accuracy)

            if not node.unlocked:
                continue

            if accuracy >= node.escalation_threshold:
                if node.current_difficulty < node.max_difficulty:
                    node.current_difficulty += 1
                    events[task_name] = f"escalated to difficulty {node.current_difficulty}"

            if accuracy >= node.mastery_threshold and not node.mastered:
                node.mastered = True
                events[task_name] = "mastered"

    def _check_unlocks(self) -> list[str]:
        """Check if any locked tasks can be unlocked based on mastered prerequisites.

        Returns:
            List of newly unlocked task names.
        """
        newly_unlocked = []

        for node in self._nodes.values():
            if node.unlocked:
                continue

            if not node.prerequisites:
                node.unlocked = True
                newly_unlocked.append(node.task_name)
                continue

            all_met = all(
                self._nodes.get(prereq, SkillNode(task_name="")).mastered
                for prereq in node.prerequisites
            )
            if all_met:
                node.unlocked = True
                newly_unlocked.append(node.task_name)

        return newly_unlocked

    def get_sampling_weights(self) -> dict[str, float]:
        """Get per-task sampling weights based on skill tree state.

        Returns:
            Dict of task_name → weight (0 for locked, 1-3 for active).
        """
        weights = {}

        for node in self._nodes.values():
            if not node.unlocked:
                weights[node.task_name] = 0.0
            elif node.mastered:
                weights[node.task_name] = self._retention_ratio
            elif node.accuracy_history and node.accuracy_history[-1] < 0.5:
                weights[node.task_name] = 3.0
            else:
                weights[node.task_name] = 2.0

        return weights

    def get_difficulty_for(self, task_name: str) -> int:
        """Get the current difficulty level for a task.

        Args:
            task_name: The task to query.

        Returns:
            Current difficulty (1 if task not found).
        """
        node = self._nodes.get(task_name)
        return node.current_difficulty if node else 1

    def get_unlocked_tasks(self) -> list[str]:
        """Return all currently unlocked task names."""
        return [n.task_name for n in self._nodes.values() if n.unlocked]

    def get_mastered_tasks(self) -> list[str]:
        """Return all mastered task names."""
        return [n.task_name for n in self._nodes.values() if n.mastered]

    def get_frontier_tasks(self) -> list[str]:
        """Return tasks that are unlocked but not yet mastered."""
        return [
            n.task_name for n in self._nodes.values()
            if n.unlocked and not n.mastered
        ]

    def summary(self) -> dict:
        """Return a summary of the skill tree state.

        Returns:
            Dict with counts and task lists.
        """
        return {
            "total": len(self._nodes),
            "unlocked": len(self.get_unlocked_tasks()),
            "mastered": len(self.get_mastered_tasks()),
            "frontier": len(self.get_frontier_tasks()),
            "locked": sum(1 for n in self._nodes.values() if not n.unlocked),
            "max_tier_reached": max(
                (n.tier for n in self._nodes.values() if n.unlocked), default=0
            ),
        }
