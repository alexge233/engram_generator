"""Skill tree and adaptive curriculum management.

Provides the generator registry (``registry.py``) for discovering and
instantiating task generators by name, and the ``SkillTree`` runtime
that tracks mastery, escalates difficulty, and unlocks prerequisite-gated
tasks as the model improves.

Modules:
    registry: Decorator-based registration, lookup by name, OOS registry.
    skill_tree: Adaptive curriculum with mastery tracking and sampling weights.
"""
