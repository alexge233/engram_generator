"""Registry of all generators and helper functions."""
from engram_generator.base import StepGenerator


_REGISTRY: dict[str, type[StepGenerator]] = {}
_OOS_REGISTRY: dict[str, type[StepGenerator]] = {}
_LOADED = False
_OOS_LOADED = False


def register(cls: type[StepGenerator]) -> type[StepGenerator]:
    """Decorator to register a generator class.

    Args:
        cls: StepGenerator subclass to register.

    Returns:
        The same class (unchanged).
    """
    instance = cls()
    _REGISTRY[instance.task_name] = cls
    return cls


def register_oos(cls: type[StepGenerator]) -> type[StepGenerator]:
    """Decorator to register an out-of-set generator.

    OOS generators are never included in training or validation.
    They are only used for final held-out evaluation.

    Args:
        cls: StepGenerator subclass to register.

    Returns:
        The same class (unchanged).
    """
    instance = cls()
    _OOS_REGISTRY[instance.task_name] = cls
    return cls


def _ensure_loaded() -> None:
    """Import all generator modules to trigger @register decorators."""
    global _LOADED
    if not _LOADED:
        import engram_generator.generators  # noqa: F401
        _LOADED = True


def get_generator(task_name: str, **kwargs) -> StepGenerator:
    """Instantiate a generator by task name.

    Args:
        task_name: Registered task name.
        **kwargs: Passed to the generator constructor.

    Returns:
        A StepGenerator instance.

    Raises:
        KeyError: If task_name is not registered.
    """
    _ensure_loaded()
    if task_name not in _REGISTRY:
        raise KeyError(
            f"Unknown task '{task_name}'. "
            f"Available: {sorted(_REGISTRY.keys())}"
        )
    return _REGISTRY[task_name](**kwargs)


def get_all_generators(**kwargs) -> list[StepGenerator]:
    """Instantiate all registered generators.

    Args:
        **kwargs: Passed to each generator constructor.

    Returns:
        List of StepGenerator instances.
    """
    _ensure_loaded()
    return [cls(**kwargs) for cls in _REGISTRY.values()]


def _ensure_oos_loaded() -> None:
    """Import OOS generator modules to trigger @register_oos decorators."""
    global _OOS_LOADED
    if not _OOS_LOADED:
        import engram_generator.generators.oos  # noqa: F401
        _OOS_LOADED = True


def get_oos_generator(task_name: str, **kwargs) -> StepGenerator:
    """Instantiate an OOS generator by task name.

    Args:
        task_name: Registered OOS task name.
        **kwargs: Passed to the generator constructor.

    Returns:
        A StepGenerator instance.

    Raises:
        KeyError: If task_name is not in OOS registry.
    """
    _ensure_oos_loaded()
    if task_name not in _OOS_REGISTRY:
        raise KeyError(f"Unknown OOS task '{task_name}'.")
    return _OOS_REGISTRY[task_name](**kwargs)


def get_all_oos_generators(**kwargs) -> list[StepGenerator]:
    """Instantiate all OOS generators for held-out evaluation.

    Args:
        **kwargs: Passed to each generator constructor.

    Returns:
        List of StepGenerator instances.
    """
    _ensure_oos_loaded()
    return [cls(**kwargs) for cls in _OOS_REGISTRY.values()]


def list_tasks() -> list[dict]:
    """List all registered tasks with metadata.

    Returns:
        List of dicts with task_name, tier, and prerequisites.
    """
    _ensure_loaded()
    result = []
    for cls in _REGISTRY.values():
        gen = cls()
        result.append({
            "task_name": gen.task_name,
            "tier": gen.tier,
            "prerequisites": gen.prerequisites,
        })
    return sorted(result, key=lambda x: (x["tier"], x["task_name"]))
