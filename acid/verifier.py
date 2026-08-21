"""
INDEPENDENT VERIFIER
Separate from discovery. Different execution strategy.
Adversarial: tries to BREAK the candidate.
"""
import time
import random
from acid.substrate import SubstrateProgram as Program, Executor, MAX_STEPS, MAX_STACK, MAX_MEMORY


class IndependentVerifier:
    """
    Verifies candidates using a DIFFERENT approach than discovery:
    - Property-based tests (not just examples)
    - Adversarial inputs
    - Determinism checking
    - Resource limit verification
    - Structural validation
    """

    def __init__(self, seed=999):
        self.rng = random.Random(seed)
        # Different executor config than discovery (stricter)
        self.executor = Executor(max_steps=MAX_STEPS // 2)

    def verify(self, program, test_cases):
        """Run all test cases independently."""
        results = []
        all_pass = True
        for inputs, expected in test_cases:
            try:
                result = self.executor.execute(program, inputs=inputs)
                if expected is None:  # FIXED: require specific behavior
                    passed = not result.get("timed_out", False) and not result.get("error", False)  # FIXED: check no crash/timeout, not just output
                else:
                    passed = result["outputs"] == expected
                results.append({
                    "inputs": inputs, "expected": expected,
                    "actual": result["outputs"], "passed": passed,
                    "steps": result["steps"]
                })
                if not passed:
                    all_pass = False
            except Exception as e:
                results.append({"inputs": inputs, "error": str(e), "passed": False})
                all_pass = False
        return {
            "verified": all_pass,
            "tests_run": len(test_cases),
            "tests_passed": sum(1 for r in results if r["passed"]),
            "results": results,
            "timestamp": time.time()
        }

    def verify_determinism(self, program, inputs, runs=5):
        """Same input must produce same output every time."""
        outputs_set = set()
        for _ in range(runs):
            result = self.executor.execute(program, inputs=inputs)
            outputs_set.add(tuple(result["outputs"]))
        return {
            "deterministic": len(outputs_set) == 1,
            "runs": runs,
            "unique_outputs": len(outputs_set)
        }

    def verify_resource_limits(self, program, inputs):
        """Check resource usage is within bounds."""
        result = self.executor.execute(program, inputs=inputs)
        return {
            "steps": result["steps"],
            "within_step_limit": result["steps"] < MAX_STEPS,
            "timed_out": result.get("timed_out", False),
            "max_allowed": MAX_STEPS
        }

    def verify_structure(self, program):
        """Structural validation of the program."""
        issues = []
        if len(program.instructions) == 0:
            issues.append("empty program")
        if len(program.instructions) > 200:
            issues.append("program too long")
        for i, (op, arg) in enumerate(program.instructions):
            if op not in ("PUSH","POP","DUP","SWAP","ADD","SUB","MUL","MOD",
                         "GT","LT","EQ","AND","OR","NOT","JZ",,"READ","WRITE","HALT"):
                issues.append(f"invalid op at {i}: {op}")
            if op == "JZ" and (arg < 0 or arg >= len(program.instructions)):
                issues.append(f"JZ target out of bounds at {i}")
        return {"valid": len(issues) == 0, "issues": issues}

    def adversarial_test(self, program, task_fn, n_tests=20):
        """
        Actively try to BREAK the candidate.
        Generate adversarial inputs and check for failures.
        """
        failures = []
        for _ in range(n_tests):
            # Adversarial inputs: empty, huge, negative-ish, single, repeated
            r = self.rng.random()
            if r < 0.2:
                inputs = []
            elif r < 0.4:
                inputs = [999999] * 3
            elif r < 0.6:
                inputs = [0, 0, 0]
            elif r < 0.8:
                inputs = [1]
            else:
                inputs = [self.rng.randint(0, 100) for _ in range(self.rng.randint(0, 5))]

            try:
                result = self.executor.execute(program, inputs=inputs)
                # Check for crashes or infinite loops
                if result["steps"] >= MAX_STEPS // 2:
                    failures.append({"inputs": inputs, "reason": "near_timeout"})
            except Exception as e:
                failures.append({"inputs": inputs, "reason": str(e)})

        return {
            "adversarial_pass": len(failures) == 0,
            "tests_run": n_tests,
            "failures": failures[:5]
        }

    def full_verify(self, program, task_fn, inputs, expected_output):
        """Complete independent verification suite."""
        test_cases = [
            (inputs, expected_output),
            ([], None),
            ([0, 0, 0], None),
            ([1, 1, 1], None),
        ]
        basic = self.verify(program, test_cases)
        determinism = self.verify_determinism(program, inputs)
        resources = self.verify_resource_limits(program, inputs)
        structure = self.verify_structure(program)
        adversarial = self.adversarial_test(program, task_fn)

        all_pass = (basic["verified"] and determinism["deterministic"]
                   and resources["within_step_limit"] and structure["valid"]
                   and adversarial["adversarial_pass"])

        return {
            "overall_pass": all_pass,
            "basic": basic,
            "determinism": determinism,
            "resources": resources,
            "structure": structure,
            "adversarial": adversarial,
            "timestamp": time.time()
        }


# ============================================================
# FIX: Multi-input verification to reject constant programs
# ============================================================

def multi_input_verify(program, task_fn, num_tests=10):
    """Verify a program against MULTIPLE random inputs.
    
    This catches constant programs like PUSH 6; WRITE; HALT
    that pass single-input tests but fail on different inputs.
    """
    import random
    rng = random.Random(42)
    
    # Generate multiple test cases
    test_cases = []
    for _ in range(num_tests):
        # Generate random inputs of varying lengths
        length = rng.randint(2, 5)
        inputs = [rng.randint(0, 50) for _ in range(length)]
        expected_sum = sum(inputs)
        test_cases.append((inputs, [expected_sum]))
    
    # Run all test cases
    passed = 0
    failed = 0
    
    for inputs, expected in test_cases:
        try:
            from acid.substrate import Executor
            ex = Executor()
            result = ex.execute(program, inputs=inputs)
            if result["outputs"] == expected:
                passed += 1
            else:
                failed += 1
        except Exception:
            failed += 1
    
    # Must pass ALL tests to be considered valid
    all_pass = (failed == 0 and passed > 0)
    
    return {
        "all_pass": all_pass,
        "passed": passed,
        "failed": failed,
        "total": num_tests,
        "is_constant": (passed <= 1),  # If only 1 passes, likely constant
    }


def detect_constant_program(program, num_tests=5):
    """Detect if a program is a constant (ignores inputs).
    
    A constant program produces the same output regardless of input.
    """
    import random
    rng = random.Random(123)
    
    from acid.substrate import Executor
    ex = Executor()
    
    outputs = []
    for _ in range(num_tests):
        inputs = [rng.randint(0, 100) for _ in range(rng.randint(2, 5))]
        try:
            result = ex.execute(program, inputs=inputs)
            outputs.append(tuple(result["outputs"]))
        except Exception:
            outputs.append(None)
    
    # If all outputs are the same, it's a constant program
    unique_outputs = set(outputs)
    is_constant = len(unique_outputs) <= 1
    
    return {
        "is_constant": is_constant,
        "unique_outputs": len(unique_outputs),
        "outputs": outputs[:3]
    }

