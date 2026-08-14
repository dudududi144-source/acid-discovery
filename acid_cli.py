#!/usr/bin/env python3
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acid.substrate import Program, Executor, validate_substrate
from acid.search import random_program
from acid.tasks import TASKS_TRAIN, TASKS_TRANSFER

def cmd_status(args):
    print("ACID System Status")
    print("=" * 40)
    print("Substrate: 18 primitives")
    print("Verification: 5 test types")
    print("Tasks: " + str(len(TASKS_TRAIN)) + " train, " + str(len(TASKS_TRANSFER)) + " transfer")

def cmd_validate(args):
    print("Validating substrate...")
    results = validate_substrate()
    for name, result in results.items():
        status = "PASS" if result.get("pass", False) else "FAIL"
        print("  [" + status + "] " + name)
    all_pass = all(r.get("pass", False) for r in results.values())
    print("Substrate valid: " + str(all_pass))

def cmd_solve(args):
    print("Solving: " + args.problem)
    inputs = json.loads(args.inputs) if args.inputs else [1, 2, 3]
    expected = json.loads(args.expected) if args.expected else [6]
    ex = Executor()
    import random
    rng = random.Random(42)
    print("Running discovery (200 gens, pop 50)...")
    best_score = 0
    best_prog = None
    total_evals = 0
    for gen in range(200):
        for _ in range(50):
            prog = random_program(rng, max_len=30)
            try:
                result = ex.execute(prog, inputs=inputs)
                total_evals += 1
                if result["outputs"] and result["outputs"][0] == expected[0]:
                    best_score = 1.0
                    best_prog = prog
                    break
            except:
                total_evals += 1
        if best_score >= 1.0:
            print("  Found at gen " + str(gen) + ", eval " + str(total_evals))
            break
        if gen % 50 == 0:
            print("  gen " + str(gen) + ", evals " + str(total_evals))
    if best_prog:
        print("SOLVED! Program: " + str(best_prog.instructions[:10]))
    else:
        print("Not found. Evals: " + str(total_evals))

def cmd_tasks(args):
    print("Training Tasks:")
    for name, task in TASKS_TRAIN.items():
        print("  " + name + ": " + task.get("description", ""))
    print("Transfer Tasks:")
    for name, task in TASKS_TRANSFER.items():
        print("  " + name + ": " + task.get("description", ""))

def cmd_bench(args):
    print("Running benchmark...")
    ex = Executor()
    import random, time
    for task_name, task in TASKS_TRAIN.items():
        inputs = task.get("inputs", [1, 2, 3])
        expected = task.get("expected_output", [6])
        rng = random.Random(42)
        start = time.time()
        found = False
        evals = 0
        for gen in range(100):
            for _ in range(30):
                prog = random_program(rng, max_len=25)
                try:
                    result = ex.execute(prog, inputs=inputs)
                    evals += 1
                    if result["outputs"] and result["outputs"][0] == expected[0]:
                        found = True
                        break
                except:
                    evals += 1
            if found:
                break
        elapsed = time.time() - start
        print("  " + task_name + ": found=" + str(found) + ", evals=" + str(evals) + ", time=" + str(round(elapsed, 2)) + "s")

def main():
    parser = argparse.ArgumentParser(description="ACID CLI")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status", help="Show system status")
    sub.add_parser("validate", help="Validate substrate")
    solve_p = sub.add_parser("solve", help="Solve a problem")
    solve_p.add_argument("problem", help="Problem description")
    solve_p.add_argument("--inputs", help="Input values (JSON array)")
    solve_p.add_argument("--expected", help="Expected output (JSON array)")
    sub.add_parser("tasks", help="List available tasks")
    sub.add_parser("bench", help="Run benchmark")
    args = parser.parse_args()
    if args.command == "status": cmd_status(args)
    elif args.command == "validate": cmd_validate(args)
    elif args.command == "solve": cmd_solve(args)
    elif args.command == "tasks": cmd_tasks(args)
    elif args.command == "bench": cmd_bench(args)
    else: parser.print_help()

if __name__ == "__main__":
    main()
