"""Parallel sample generation using multiprocessing.

Bypasses the GIL by spawning separate processes, each with its
own generator instance and independent random seed. Samples are
generated in true parallel across CPU cores.
"""
from concurrent.futures import ProcessPoolExecutor
from typing import Type

from engram_generator.base import Sample, StepGenerator


def _worker_generate(args: tuple) -> list[Sample]:
    """Generate samples in a worker process.

    Each worker gets its own generator instance with a unique seed,
    ensuring no shared state and true parallel execution.

    Args:
        args: Tuple of (generator_class, num_samples, min_diff, max_diff, seed).

    Returns:
        List of generated samples.
    """
    cls, num_samples, min_diff, max_diff, seed = args
    gen = cls(min_difficulty=min_diff, max_difficulty=max_diff, seed=seed)
    return gen.generate(num_samples)


class ParallelGenerator:
    """Generates samples across multiple processes.

    Distributes work evenly across CPU cores. Each process gets
    its own generator instance with a unique seed derived from
    the base seed, ensuring reproducibility and no GIL contention.

    Attributes:
        max_workers: Number of parallel processes.

    Example:
        >>> from engram_generator.generators.tier0 import AdditionGenerator
        >>> pg = ParallelGenerator(max_workers=4)
        >>> samples = pg.generate(AdditionGenerator, num_samples=10000)
        >>> len(samples)
        10000
    """

    def __init__(self, max_workers: int | None = None) -> None:
        """Initialise the parallel generator.

        Args:
            max_workers: Number of processes. None uses all CPU cores.
        """
        self._max_workers = max_workers

    def generate(self, generator_class: Type[StepGenerator],
                 num_samples: int,
                 min_difficulty: int = 1,
                 max_difficulty: int = 8,
                 base_seed: int = 42) -> list[Sample]:
        """Generate samples in parallel across multiple processes.

        Args:
            generator_class: The StepGenerator subclass to use.
            num_samples: Total number of samples to generate.
            min_difficulty: Minimum difficulty level.
            max_difficulty: Maximum difficulty level.
            base_seed: Base seed (each worker gets base_seed + worker_id).

        Returns:
            Combined list of samples from all workers.
        """
        chunks = self._split_work(num_samples)
        args = self._build_worker_args(
            generator_class, chunks, min_difficulty, max_difficulty, base_seed,
        )
        return self._execute(args)

    def generate_mixed(self, generator_classes: list[Type[StepGenerator]],
                       samples_per_task: int,
                       min_difficulty: int = 1,
                       max_difficulty: int = 8,
                       base_seed: int = 42) -> list[Sample]:
        """Generate samples from multiple generators in parallel.

        Each generator runs in its own process. True parallelism
        across different task types.

        Args:
            generator_classes: List of StepGenerator subclasses.
            samples_per_task: Number of samples per generator.
            min_difficulty: Minimum difficulty level.
            max_difficulty: Maximum difficulty level.
            base_seed: Base seed (each task gets a unique seed).

        Returns:
            Combined list of samples from all generators.
        """
        args = [
            (cls, samples_per_task, min_difficulty, max_difficulty, base_seed + i)
            for i, cls in enumerate(generator_classes)
        ]
        return self._execute(args)

    def _split_work(self, total: int) -> list[int]:
        """Split total samples evenly across workers.

        Args:
            total: Total number of samples.

        Returns:
            List of per-worker sample counts.
        """
        workers = self._effective_workers()
        base = total // workers
        remainder = total % workers

        chunks = [base + (1 if i < remainder else 0) for i in range(workers)]
        return chunks

    def _effective_workers(self) -> int:
        """Return the number of workers to use.

        Returns:
            Number of processes, defaulting to CPU count.
        """
        if self._max_workers is not None:
            return self._max_workers

        import os
        return os.cpu_count() or 4

    def _build_worker_args(self, generator_class: Type[StepGenerator],
                           chunks: list[int],
                           min_difficulty: int,
                           max_difficulty: int,
                           base_seed: int) -> list[tuple]:
        """Build argument tuples for each worker.

        Args:
            generator_class: Generator class for all workers.
            chunks: Per-worker sample counts.
            min_difficulty: Min difficulty.
            max_difficulty: Max difficulty.
            base_seed: Base seed.

        Returns:
            List of argument tuples for _worker_generate.
        """
        return [
            (generator_class, count, min_difficulty, max_difficulty, base_seed + i)
            for i, count in enumerate(chunks)
        ]

    def _execute(self, args: list[tuple]) -> list[Sample]:
        """Execute workers and collect results.

        Args:
            args: List of argument tuples for _worker_generate.

        Returns:
            Flat list of all generated samples.
        """
        with ProcessPoolExecutor(max_workers=self._max_workers) as pool:
            results = list(pool.map(_worker_generate, args))

        samples: list[Sample] = []
        for batch in results:
            samples.extend(batch)
        return samples
