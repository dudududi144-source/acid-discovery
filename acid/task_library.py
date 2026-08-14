"""
ACID Task Library
Comprehensive task definitions for discovery experiments.
"""

# Task categories
CATEGORIES = {
    "arithmetic": "Basic arithmetic operations",
    "comparison": "Comparison and selection",
    "io_pattern": "Input/output patterns",
    "accumulation": "Accumulation and reduction",
    "conditional": "Conditional execution",
    "iteration": "Iterative computation"
}

# Task definitions
TASKS = {
    # Arithmetic
    "sum_2": {
        "category": "arithmetic",
        "description": "Sum of 2 inputs",
        "inputs": [2, 3],
        "expected": [5],
        "difficulty": 1,
        "min_ops": 4
    },
    "sum_3": {
        "category": "arithmetic",
        "description": "Sum of 3 inputs",
        "inputs": [1, 2, 3],
        "expected": [6],
        "difficulty": 2,
        "min_ops": 6
    },
    "sum_4": {
        "category": "arithmetic",
        "description": "Sum of 4 inputs",
        "inputs": [1, 2, 3, 4],
        "expected": [10],
        "difficulty": 3,
        "min_ops": 8
    },
    "sum_6": {
        "category": "arithmetic",
        "description": "Sum of 6 inputs",
        "inputs": [1, 2, 3, 4, 5, 6],
        "expected": [21],
        "difficulty": 4,
        "min_ops": 12
    },
    "sum_8": {
        "category": "arithmetic",
        "description": "Sum of 8 inputs",
        "inputs": [1, 2, 3, 4, 5, 6, 7, 8],
        "expected": [36],
        "difficulty": 5,
        "min_ops": 16
    },
    "product_2": {
        "category": "arithmetic",
        "description": "Product of 2 inputs",
        "inputs": [3, 4],
        "expected": [12],
        "difficulty": 2,
        "min_ops": 4
    },
    "diff_2": {
        "category": "arithmetic",
        "description": "Difference of 2 inputs",
        "inputs": [7, 3],
        "expected": [4],
        "difficulty": 1,
        "min_ops": 4
    },
    
    # Comparison
    "max_2": {
        "category": "comparison",
        "description": "Maximum of 2 inputs",
        "inputs": [3, 7],
        "expected": [7],
        "difficulty": 3,
        "min_ops": 6
    },
    "max_3": {
        "category": "comparison",
        "description": "Maximum of 3 inputs",
        "inputs": [3, 9, 5],
        "expected": [9],
        "difficulty": 4,
        "min_ops": 10
    },
    "min_2": {
        "category": "comparison",
        "description": "Minimum of 2 inputs",
        "inputs": [3, 7],
        "expected": [3],
        "difficulty": 3,
        "min_ops": 6
    },
    
    # Accumulation
    "cumulative_sum": {
        "category": "accumulation",
        "description": "Cumulative sum (output running total)",
        "inputs": [3, 2],
        "expected": [3, 5],
        "difficulty": 4,
        "min_ops": 8
    },
    
    # Conditional
    "abs_diff": {
        "category": "conditional",
        "description": "Absolute difference of 2 inputs",
        "inputs": [3, 7],
        "expected": [4],
        "difficulty": 5,
        "min_ops": 10
    }
}

def get_tasks_by_category(category):
    """Get all tasks in a category."""
    return {k: v for k, v in TASKS.items() if v["category"] == category}

def get_tasks_by_difficulty(max_difficulty):
    """Get tasks up to a difficulty level."""
    return {k: v for k, v in TASKS.items() if v["difficulty"] <= max_difficulty}

def get_task(name):
    """Get a specific task by name."""
    return TASKS.get(name)

def list_tasks():
    """List all tasks with metadata."""
    return [
        {
            "name": name,
            "category": task["category"],
            "description": task["description"],
            "difficulty": task["difficulty"]
        }
        for name, task in TASKS.items()
    ]

def get_transfer_pairs():
    """Get recommended transfer pairs (source -> target)."""
    return [
        ("sum_3", "sum_4"),
        ("sum_4", "sum_6"),
        ("sum_6", "sum_8"),
        ("max_2", "max_3"),
        ("sum_3", "cumulative_sum"),
        ("product_2", "sum_2")
    ]
