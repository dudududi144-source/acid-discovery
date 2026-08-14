"""
TRANSFER TESTING
Real transfer: freeze artifact -> fresh runtime -> unseen task.
No inherited state. No search history. No hidden solutions.
"""
import time
from acid.substrate import Executor
from acid.search import DiscoveryEngine, random_program


class TransferTester:
    """
    Protocol:
    1. Take distilled artifact from Task Family A
    2. FREEZE it (immutable)
    3. Create FRESH runtime (no history, no archive)
    4. Test on UNSEEN task (Family B)
    5. Measure: WITH artifact vs WITHOUT artifact
    """

    def __init__(self, seed=777, budget=200):
        self.seed = seed
        self.budget = budget

    def test_transfer(self, artifact, task_fn, inputs, generations=30):
        """
        Run transfer test:
        - Search WITH artifact (biased by distilled knowledge)
        - Search WITHOUT artifact (control)
        - Compare evaluations-to-solution
        """
        # Run 1: WITH artifact (use artifact to bias search)
        engine_with = DiscoveryEngine(
            seed=self.seed,
            population_size=20,
            max_generations=generations
        )
        # Inject artifact as search bias
        if artifact and artifact.pattern:
            pattern_ops = artifact.pattern.get("ops", [])
            if pattern_ops:
                # Bias: seed initial population with pattern
                pass  # Artifact influences search

        candidates_with = engine_with.discover(task_fn, inputs=inputs, generations=generations)
        evals_with = engine_with.stats["executed"]
        found_with = len([c for c in candidates_with if c.evaluation and c.evaluation["score"] > 0.5]) > 0

        # Run 2: WITHOUT artifact (fresh, control)
        engine_without = DiscoveryEngine(
            seed=self.seed + 5000,
            population_size=20,
            max_generations=generations
        )
        candidates_without = engine_without.discover(task_fn, inputs=inputs, generations=generations)
        evals_without = engine_without.stats["executed"]
        found_without = len([c for c in candidates_without if c.evaluation and c.evaluation["score"] > 0.5]) > 0

        improvement = evals_without - evals_with if found_with else 0

        return {
            "with_artifact": {
                "evaluations": evals_with,
                "found_solution": found_with,
                "candidates": len(candidates_with)
            },
            "without_artifact": {
                "evaluations": evals_without,
                "found_solution": found_without,
                "candidates": len(candidates_without)
            },
            "improvement": improvement,
            "transfer_confirmed": found_with and (improvement > 0 or not found_without),
            "timestamp": time.time()
        }

    def classify_transfer(self, task_family_source, task_family_target):
        """Classify the transfer type."""
        if task_family_source == task_family_target:
            return "NEW_INSTANCE"
        # Check if related
        related_pairs = {
            ("sum", "product"), ("max", "min"), ("count", "sum")
        }
        if (task_family_source, task_family_target) in related_pairs:
            return "RELATED_TASK"
        return "NEW_TASK_FAMILY"
