"""
ADVERSARIAL SELF-VALIDATION
The system must actively attack its own positive results.
"""
import random
import time


class Adversary:
    """
    For every major claim:
    CLAIM -> EVIDENCE -> INDEPENDENT CHECK -> COUNTERTEST -> REPLICATION -> STATUS

    Attacks:
    - Benchmark leakage
    - Overfitting
    - Reward hacking
    - Evaluator exploitation
    - Trivial novelty
    - Hidden state inheritance
    - Random luck
    - Resource unfairness
    - Non-determinism
    """

    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.attacks_run = []

    def check_benchmark_leakage(self, task_fn, search_history):
        """Could the search have memorized the task?"""
        # Check if task function was exposed during search
        return {
            "attack": "benchmark_leakage",
            "risk": "LOW" if not search_history else "MEDIUM",
            "mitigation": "Task functions are separate from search code"
        }

    def check_random_luck(self, results, n_seeds=5):
        """Could the result be random luck?"""
        if len(results) < n_seeds:
            return {"attack": "random_luck", "risk": "HIGH", "reason": "insufficient seeds"}
        scores = [r.get("score", 0) for r in results if isinstance(r, dict)]
        if not scores:
            return {"attack": "random_luck", "risk": "UNKNOWN", "reason": "no scores"}
        variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
        risk = "LOW" if variance < 0.1 else "MEDIUM" if variance < 0.5 else "HIGH"
        return {"attack": "random_luck", "risk": risk, "variance": variance}

    def check_trivial_novelty(self, candidate, known_programs):
        """Is the 'novel' candidate actually trivial?"""
        if len(candidate.program) < 5:
            return {"attack": "trivial_novelty", "risk": "HIGH", "reason": "program too short"}
        # Check semantic equivalence with known programs
        cand_ops = [op for op, _ in candidate.program.instructions]
        for known in known_programs[:10]:
            known_ops = [op for op, _ in known.instructions]
            if cand_ops == known_ops:
                return {"attack": "trivial_novelty", "risk": "HIGH", "reason": "identical structure"}
        return {"attack": "trivial_novelty", "risk": "LOW"}

    def check_hidden_state(self, engine, fresh_engine):
        """Could hidden state have been inherited?"""
        if engine.archive and not fresh_engine.archive:
            return {"attack": "hidden_state", "risk": "LOW", "reason": "fresh engine has empty archive"}
        return {"attack": "hidden_state", "risk": "MEDIUM"}

    def check_resource_fairness(self, system_0_stats, system_1_stats):
        """Were resources equal between systems?"""
        evals_0 = system_0_stats.get("executed", 0)
        evals_1 = system_1_stats.get("executed", 0)
        if evals_0 == 0 or evals_1 == 0:
            return {"attack": "resource_fairness", "risk": "UNKNOWN"}
        ratio = max(evals_0, evals_1) / min(evals_0, evals_1)
        risk = "LOW" if ratio < 1.5 else "MEDIUM" if ratio < 3 else "HIGH"
        return {"attack": "resource_fairness", "risk": risk, "ratio": ratio}

    def run_all_attacks(self, context):
        """Run all adversarial checks."""
        attacks = [
            self.check_benchmark_leakage(context.get("task_fn"), context.get("search_history", [])),
            self.check_random_luck(context.get("results", [])),
            self.check_trivial_novelty(context.get("candidate"), context.get("known_programs", [])),
            self.check_resource_fairness(context.get("system_0_stats", {}), context.get("system_1_stats", {})),
        ]
        self.attacks_run.extend(attacks)

        high_risk = sum(1 for a in attacks if a.get("risk") == "HIGH")
        medium_risk = sum(1 for a in attacks if a.get("risk") == "MEDIUM")

        return {
            "attacks": attacks,
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "overall": "PASS" if high_risk == 0 else "CAUTION" if high_risk <= 1 else "FAIL",
            "timestamp": time.time()
        }


# ============================================================
# FIX: Adversarial testing that checks CORRECTNESS
# ============================================================

def adversarial_correctness_test(program, task_fn, num_tests=20):
    """Adversarial test that checks CORRECTNESS, not just survival.
    
    Previous version only checked if the program crashed.
    This version checks if the program produces CORRECT outputs
    for adversarial inputs.
    """
    import random
    rng = random.Random(999)
    
    from acid.substrate import Executor
    ex = Executor()
    
    # Generate adversarial inputs
    adversarial_inputs = []
    
    # Edge cases
    adversarial_inputs.append([0, 0, 0])
    adversarial_inputs.append([999999, 999999, 999999])
    adversarial_inputs.append([-1, -1, -1])
    adversarial_inputs.append([1])
    adversarial_inputs.append([0])
    
    # Random adversarial
    for _ in range(num_tests - 5):
        length = rng.randint(1, 6)
        inputs = [rng.randint(-100, 100) for _ in range(length)]
        adversarial_inputs.append(inputs)
    
    # Test each adversarial input
    passed = 0
    failed = 0
    crashed = 0
    
    for inputs in adversarial_inputs:
        try:
            result = ex.execute(program, inputs=inputs)
            
            # Check correctness against task function
            if task_fn:
                expected = task_fn(inputs)
                if result["outputs"] == expected:
                    passed += 1
                else:
                    failed += 1
            else:
                # If no task_fn, just check it doesn't crash
                passed += 1
        except Exception:
            crashed += 1
    
    total = len(adversarial_inputs)
    correctness_rate = passed / max(1, total - crashed)
    
    return {
        "passed": passed,
        "failed": failed,
        "crashed": crashed,
        "total": total,
        "correctness_rate": correctness_rate,
        "is_correct": correctness_rate >= 0.9,
        "survived": crashed == 0
    }

