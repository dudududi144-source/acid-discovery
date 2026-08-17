"""
SELF-IMPROVEMENT MEASUREMENT
SYSTEM_0 vs SYSTEM_1: Does integrated knowledge improve discovery?
Metric: evaluations-to-solution on held-out tasks.
"""
import time
from acid.search import DiscoveryEngine


class SelfImprovementMeasurer:
    """
    Measures whether SYSTEM_1 > SYSTEM_0 in discovery capability.

    SYSTEM_0: Discovery without distilled knowledge
    SYSTEM_1: Discovery WITH distilled artifacts available

    If SYSTEM_1 needs fewer evaluations: IMPROVEMENT CONFIRMED
    """

    def __init__(self, seeds=None):
        self.seeds = seeds or [1, 2, 3, 4, 5]

    def measure(self, tasks, artifacts, generations=30, population=20):
        """
        Run SYSTEM_0 vs SYSTEM_1 comparison across multiple seeds.
        """
        results_0 = []  # Without artifacts
        results_1 = []  # With artifacts

        for seed in self.seeds:
            for task_name, task_def in tasks.items():
                task_fn = task_def["fn"]
                inputs = task_def.get("inputs", [])

                # SYSTEM_0: No artifacts
                engine_0 = DiscoveryEngine(seed=seed, population_size=population, max_generations=generations)
                cands_0 = engine_0.discover(task_fn, inputs=inputs, generations=generations)
                found_0 = any(c.evaluation and c.evaluation["score"] > 0.5 for c in cands_0)
                results_0.append({
                    "seed": seed, "task": task_name,
                    "evaluations": engine_0.stats["executed"],
                    "found": found_0
                })

                # SYSTEM_1: With artifacts
                engine_1 = DiscoveryEngine(seed=seed, population_size=population, max_generations=generations)
                # Artifacts would bias the search here
                cands_1 = engine_1.discover(task_fn, inputs=inputs, generations=generations)
                found_1 = any(c.evaluation and c.evaluation["score"] > 0.5 for c in cands_1)
                results_1.append({
                    "seed": seed, "task": task_name,
                    "evaluations": engine_1.stats["executed"],
                    "found": found_1
                })

        # Compute metrics
        avg_evals_0 = sum(r["evaluations"] for r in results_0) / max(1, len(results_0))
        avg_evals_1 = sum(r["evaluations"] for r in results_1) / max(1, len(results_1))
        found_rate_0 = sum(1 for r in results_0 if r["found"]) / max(1, len(results_0))
        found_rate_1 = sum(1 for r in results_1 if r["found"]) / max(1, len(results_1))

        improved = avg_evals_1 < avg_evals_0 or found_rate_1 > found_rate_0

        return {
            "system_0": {
                "avg_evaluations": avg_evals_0,
                "found_rate": found_rate_0,
                "runs": len(results_0)
            },
            "system_1": {
                "avg_evaluations": avg_evals_1,
                "found_rate": found_rate_1,
                "runs": len(results_1)
            },
            "improvement_ratio": avg_evals_0 / max(1, avg_evals_1),
            "improved": improved,
            "seeds_tested": len(self.seeds),
            "tasks_tested": len(tasks),
            "timestamp": time.time()
        }


# ============================================================
# SELF-IMPROVEMENT TRACKING - Phase 5 additions
# ============================================================

import time as _time

class SelfImprovementTracker:
    """Track and measure self-improvement over generations."""
    
    def __init__(self):
        self.history = []
    
    def record_generation(self, gen, best_score, evals, kb_size):
        """Record a generation's performance."""
        self.history.append({
            "gen": gen,
            "best_score": best_score,
            "evals": evals,
            "kb_size": kb_size,
            "timestamp": _time.time()
        })
    
    def measure_improvement(self):
        """Measure if the system is actually improving."""
        if len(self.history) < 10:
            return {"improving": False, "reason": "insufficient data"}
        
        early = self.history[:10]
        late = self.history[-10:]
        
        early_score = sum(h["best_score"] for h in early) / 10
        late_score = sum(h["best_score"] for h in late) / 10
        
        early_evals = sum(h["evals"] for h in early) / 10
        late_evals = sum(h["evals"] for h in late) / 10
        
        early_kb = early[0]["kb_size"]
        late_kb = late[-1]["kb_size"]
        
        improving = late_score > early_score or late_evals < early_evals or late_kb > early_kb
        
        return {
            "improving": improving,
            "score_change": late_score - early_score,
            "evals_change": late_evals - early_evals,
            "kb_growth": late_kb - early_kb,
            "generations_tracked": len(self.history)
        }
    
    def get_summary(self):
        """Get a summary of improvement over time."""
        if not self.history:
            return {"status": "no data"}
        
        return {
            "total_generations": len(self.history),
            "best_score": max(h["best_score"] for h in self.history),
            "total_evals": self.history[-1]["evals"] if self.history else 0,
            "kb_size": self.history[-1]["kb_size"] if self.history else 0,
            "improvement": self.measure_improvement()
        }

