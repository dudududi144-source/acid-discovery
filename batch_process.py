#!/usr/bin/env python3
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acid.substrate import Program, Executor
from acid.search import random_program
from acid.tasks import TASKS_TRAIN, TASKS_TRANSFER

def run_batch(tasks, generations=100, pop_size=30, seed=42):
    ex = Executor()
    import random
    results = {}
    for task_name, task in tasks.items():
        inputs = task.get("inputs", [1, 2, 3])
        expected = task.get("expected_output", [6])
        task_fn = task.get("fn")
        rng = random.Random(seed)
        start = time.time()
        found = False
        evals = 0
        best_score = 0
        for gen in range(generations):
            for _ in range(pop_size):
                prog = random_program(rng, max_len=25)
                try:
                    result = ex.execute(prog, inputs=inputs)
                    evals += 1
                    score = task_fn(result) if task_fn else 0
                    if score > best_score:
                        best_score = score
                    if score >= 1.0:
                        found = True
                        break
                except:
                    evals += 1
            if found:
                break
        elapsed = time.time() - start
        results[task_name] = {
            "found": found,
            "evals": evals,
            "time": round(elapsed, 2),
            "best_score": best_score
        }
        print("  " + task_name + ": found=" + str(found) + ", evals=" + str(evals) + ", time=" + str(round(elapsed, 2)) + "s")
    return results

def main():
    print("ACID Batch Processing")
    print("=" * 40)
    print("Running training tasks...")
    train_results = run_batch(TASKS_TRAIN, generations=100, pop_size=30)
    print("Running transfer tasks...")
    transfer_results = run_batch(TASKS_TRANSFER, generations=100, pop_size=30)
    print("=" * 40)
    print("Summary:")
    train_found = sum(1 for r in train_results.values() if r["found"])
    transfer_found = sum(1 for r in transfer_results.values() if r["found"])
    print("  Training: " + str(train_found) + "/" + str(len(train_results)) + " found")
    print("  Transfer: " + str(transfer_found) + "/" + str(len(transfer_results)) + " found")
    output = {
        "training": train_results,
        "transfer": transfer_results,
        "summary": {
            "training_found": train_found,
            "training_total": len(train_results),
            "transfer_found": transfer_found,
            "transfer_total": len(transfer_results)
        }
    }
    os.makedirs("output", exist_ok=True)
    with open("output/batch_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Results saved to output/batch_results.json")

if __name__ == "__main__":
    main()
