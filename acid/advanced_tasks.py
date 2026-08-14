"""
ACID Advanced Tasks
Complex tasks that require composition and abstraction.
"""

ADVANCED_TASKS = {
    # Composition tasks
    "weighted_sum": {
        "category": "composition",
        "description": "Weighted sum: a*2 + b*3 + c",
        "inputs": [1, 2, 3],
        "expected": [11],
        "difficulty": 6,
        "requires": ["MUL", "ADD", "READ"]
    },
    "running_average": {
        "category": "composition",
        "description": "Running average of inputs",
        "inputs": [2, 4, 6],
        "expected": [4],
        "difficulty": 7,
        "requires": ["ADD", "READ", "MUL"]
    },
    
    # Conditional tasks
    "clamp": {
        "category": "conditional",
        "description": "Clamp input to range [0, 10]",
        "inputs": [15],
        "expected": [10],
        "difficulty": 6,
        "requires": ["GT", "LT", "READ", "WRITE"]
    },
    "sign": {
        "category": "conditional",
        "description": "Return sign of input (-1, 0, or 1)",
        "inputs": [5],
        "expected": [1],
        "difficulty": 7,
        "requires": ["GT", "LT", "EQ", "READ", "WRITE"]
    },
    
    # Iterative tasks
    "count_down": {
        "category": "iteration",
        "description": "Count down from input to 0",
        "inputs": [3],
        "expected": [3, 2, 1, 0],
        "difficulty": 8,
        "requires": ["SUB", "WRITE", "JZ"]
    },
    "fibonacci_5": {
        "category": "iteration",
        "description": "First 5 Fibonacci numbers",
        "inputs": [],
        "expected": [1, 1, 2, 3, 5],
        "difficulty": 9,
        "requires": ["ADD", "DUP", "SWAP", "WRITE"]
    },
    
    # Abstraction tasks
    "apply_twice": {
        "category": "abstraction",
        "description": "Apply operation twice: (x+1)+1",
        "inputs": [3],
        "expected": [5],
        "difficulty": 5,
        "requires": ["ADD", "DUP"]
    },
    "compose_ops": {
        "category": "abstraction",
        "description": "Compose: (a+b)*2",
        "inputs": [2, 3],
        "expected": [10],
        "difficulty": 6,
        "requires": ["ADD", "MUL", "READ"]
    }
}


def get_advanced_tasks_by_difficulty(min_difficulty, max_difficulty=None):
    """Get advanced tasks within difficulty range."""
    results = {}
    for name, task in ADVANCED_TASKS.items():
        diff = task["difficulty"]
        if diff >= min_difficulty:
            if max_difficulty is None or diff <= max_difficulty:
                results[name] = task
    return results


def get_tasks_requiring(primitive):
    """Get tasks that require a specific primitive."""
    return {
        k: v for k, v in ADVANCED_TASKS.items()
        if primitive in v.get("requires", [])
    }


def get_composition_chain():
    """Get tasks in order of composition complexity."""
    return sorted(
        ADVANCED_TASKS.items(),
        key=lambda x: x[1]["difficulty"]
    )


def validate_advanced_task(name, program_output):
    """Validate output for an advanced task."""
    if name not in ADVANCED_TASKS:
        return False
    
    task = ADVANCED_TASKS[name]
    expected = task["expected"]
    
    if len(program_output) != len(expected):
        return False
    
    return all(a == b for a, b in zip(program_output, expected))
