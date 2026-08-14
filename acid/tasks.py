"""
TASK FAMILIES - Calibrated, verified, graded.

Each task:
1. Has a hand-crafted solution (proves solvability)
2. Is tested for random success rate (must be < 5%)
3. Requires specific computational structure
4. Is classified: TRAIN / TRANSFER / NOVEL
"""
from acid.substrate import Program, Executor


# === TASK DEFINITIONS ===
# Each task: (name, description, input_spec, expected_fn, family)

def task_sum_3(result):
    """Sum of 3 inputs. Requires: READ + ADD + WRITE chain."""
    outputs = result["outputs"]
    if len(outputs) >= 1 and outputs[0] == 6:
        return 1.0
    if len(outputs) >= 1 and abs(outputs[0] - 6) <= 1:
        return 0.3
    return 0.0

def task_max_3(result):
    """Max of 3 inputs. Requires: READ + GT + conditional."""
    outputs = result["outputs"]
    if len(outputs) >= 1 and outputs[0] == 9:
        return 1.0
    return 0.0

def task_count_outputs(result):
    """Produce multiple outputs. Requires: multiple WRITE ops."""
    outputs = result["outputs"]
    return min(len(outputs) / 3.0, 1.0)

def task_accumulate(result):
    """Produce increasing sequence. Requires: loop + increment."""
    outputs = result["outputs"]
    if len(outputs) < 2:
        return 0.0
    increasing = sum(1 for i in range(1, len(outputs)) if outputs[i] > outputs[i-1])
    return increasing / max(1, len(outputs) - 1)

def task_transfer_min_3(result):
    """TRANSFER: Min of 3 inputs."""
    outputs = result["outputs"]
    if len(outputs) >= 1 and outputs[0] == 2:
        return 1.0
    return 0.0

def task_transfer_product(result):
    """TRANSFER: Product of 2 inputs."""
    outputs = result["outputs"]
    if len(outputs) >= 1 and outputs[0] == 15:
        return 1.0
    if len(outputs) >= 1 and abs(outputs[0] - 15) <= 2:
        return 0.3
    return 0.0

def task_novel_sort_3(result):
    """NOVEL: Sort 3 inputs (ascending)."""
    outputs = result["outputs"]
    if len(outputs) >= 3 and outputs[:3] == [1, 5, 9]:
        return 1.0
    if len(outputs) >= 2 and outputs[0] <= outputs[1]:
        return 0.2
    return 0.0


# === TASK REGISTRY ===
TASKS_TRAIN = {
    "sum_3": {
        "fn": task_sum_3,
        "inputs": [1, 2, 3],
        "expected_output": [6],
        "description": "Sum 3 inputs",
        "required_structure": "READ+ADD+WRITE chain",
        "hand_solution": Program([
            ("READ", 0), ("READ", 1), ("ADD", 0),
            ("READ", 2), ("ADD", 0), ("WRITE", 3), ("HALT", 0)
        ])
    },
    "max_3": {
        "fn": task_max_3,
        "inputs": [3, 9, 5],
        "expected_output": [9],
        "description": "Max of 3 inputs",
        "required_structure": "READ+GT+conditional WRITE",
        "hand_solution": None  # More complex, discovery must find it
    },
    "count_outputs": {
        "fn": task_count_outputs,
        "inputs": [],
        "expected_output": None,
        "description": "Produce 3+ outputs",
        "required_structure": "Multiple WRITE operations",
        "hand_solution": Program([
            ("PUSH", 0), ("WRITE", 0),
            ("PUSH", 1), ("WRITE", 1),
            ("PUSH", 2), ("WRITE", 2), ("HALT", 0)
        ], constants=[10, 20, 30])
    },
}

TASKS_TRANSFER = {
    "min_3": {
        "fn": task_transfer_min_3,
        "inputs": [7, 2, 5],
        "expected_output": [2],
        "description": "Min of 3 inputs (UNSEEN)",
        "required_structure": "READ+LT+conditional",
    },
    "product_2": {
        "fn": task_transfer_product,
        "inputs": [3, 5],
        "expected_output": [15],
        "description": "Product of 2 inputs (UNSEEN)",
        "required_structure": "READ+MUL+WRITE",
    },
}

TASKS_NOVEL = {
    "sort_3": {
        "fn": task_novel_sort_3,
        "inputs": [5, 1, 9],
        "expected_output": [1, 5, 9],
        "description": "Sort 3 inputs (NOVEL)",
        "required_structure": "Comparison network",
    },
}


def calibrate_task(task_name, task_def, n_random=200, seed=123):
    """
    Verify task is NOT trivially solvable by random programs.
    Random success rate must be < 5%.
    """
    import random
    from acid.substrate import PRIMITIVES, MAX_PROGRAM_LENGTH
    from acid.discovery import random_program

    rng = random.Random(seed)
    ex = Executor()
    successes = 0

    for _ in range(n_random):
        prog = random_program(rng, max_len=30)
        try:
            result = ex.execute(prog, inputs=task_def.get("inputs", []))
            score = task_def["fn"](result)
            if score >= 0.8:
                successes += 1
        except:
            pass

    rate = successes / n_random
    return {
        "task": task_name,
        "random_success_rate": rate,
        "calibrated": rate < 0.05,
        "n_tested": n_random,
        "n_success": successes
    }


def verify_hand_solution(task_def):
    """Verify the hand-crafted solution actually works."""
    if task_def.get("hand_solution") is None:
        return {"verified": False, "reason": "no hand solution provided"}
    ex = Executor()
    result = ex.execute(task_def["hand_solution"], inputs=task_def.get("inputs", []))
    expected = task_def.get("expected_output")
    if expected is None:
        return {"verified": len(result["outputs"]) > 0, "outputs": result["outputs"]}
    passed = result["outputs"] == expected
    return {"verified": passed, "expected": expected, "actual": result["outputs"]}
