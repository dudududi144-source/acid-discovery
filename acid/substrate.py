"""
ACID SUBSTRATE - Minimal computational substrate.
18 primitives. Deterministic. Bounded. No intelligence embedded.

CRITICAL: This module includes self-validation.
The substrate PROVES it can compute before discovery begins.
"""
import hashlib
import json

# === PRIMITIVES (18 total) ===
PRIMITIVES = [
    "PUSH", "POP", "DUP", "SWAP",
    "ADD", "SUB", "MUL", "MOD",
    "GT", "LT", "EQ",
    "AND", "OR", "NOT",
    "JZ", "LOOP",
    "READ", "WRITE",
    "HALT"
]
PRIMITIVE_COUNT = len(PRIMITIVES)  # 19 with HALT

# === BOUNDS ===
MAX_STACK = 256
MAX_MEMORY = 64
MAX_STEPS = 10000
MAX_PROGRAM_LENGTH = 200
MAX_LOOP_ITER = 100
VALUE_MOD = 1000000


class Program:
    """A program in the substrate language."""
    def __init__(self, instructions, constants=None):
        self.instructions = instructions  # list of (opcode_str, int_arg)
        self.constants = constants or []
        self._hash = None

    def canonical(self):
        return json.dumps({"i": self.instructions, "c": self.constants}, sort_keys=True)

    def hash(self):
        if self._hash is None:
            self._hash = hashlib.sha256(self.canonical().encode()).hexdigest()[:16]
        return self._hash

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return f"Program({self.hash()}, len={len(self)})"


class Executor:
    """Executes substrate programs with strict resource bounds."""

    def __init__(self, max_steps=MAX_STEPS):
        self.max_steps = max_steps

    def execute(self, program, inputs=None):
        stack = []
        memory = [0] * MAX_MEMORY
        inputs = list(inputs or [])
        input_idx = 0
        outputs = []
        pc = 0
        steps = 0
        instr = program.instructions
        consts = program.constants
        n_instr = len(instr)

        while pc < n_instr and steps < self.max_steps:
            op, arg = instr[pc]
            steps += 1

            if op == "HALT":
                break
            elif op == "PUSH":
                if len(stack) < MAX_STACK:
                    val = consts[arg % len(consts)] if consts else (arg % 100)
                    stack.append(val)
            elif op == "POP":
                if stack:
                    stack.pop()
            elif op == "DUP":
                if stack and len(stack) < MAX_STACK:
                    stack.append(stack[-1])
            elif op == "SWAP":
                if len(stack) >= 2:
                    stack[-1], stack[-2] = stack[-2], stack[-1]
            elif op == "ADD":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append((a + b) % VALUE_MOD)
            elif op == "SUB":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append((a - b) % VALUE_MOD)
            elif op == "MUL":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append((a * b) % VALUE_MOD)
            elif op == "MOD":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(a % b if b != 0 else 0)
            elif op == "GT":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(1 if a > b else 0)
            elif op == "LT":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(1 if a < b else 0)
            elif op == "EQ":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(1 if a == b else 0)
            elif op == "AND":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(1 if (a != 0 and b != 0) else 0)
            elif op == "OR":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append(1 if (a != 0 or b != 0) else 0)
            elif op == "NOT":
                if stack:
                    stack.append(0 if stack.pop() != 0 else 1)
            elif op == "JZ":
                if stack:
                    val = stack.pop()
                    if val == 0:
                        target = arg % n_instr
                        if 0 <= target < n_instr:
                            pc = target
                            continue
            elif op == "LOOP":
                # Bounded loop: repeat next instruction arg times (max MAX_LOOP_ITER)
                count = min(arg % MAX_LOOP_ITER, MAX_LOOP_ITER)
                if pc + 1 < n_instr and count > 0:
                    for _ in range(count):
                        if steps >= self.max_steps:
                            break
                        steps += 1
                        loop_op, loop_arg = instr[pc + 1]
                        if loop_op == "PUSH" and len(stack) < MAX_STACK:
                            stack.append(consts[loop_arg % len(consts)] if consts else (loop_arg % 100))
                        elif loop_op == "ADD" and len(stack) >= 2:
                            b, a = stack.pop(), stack.pop()
                            stack.append((a + b) % VALUE_MOD)
                        elif loop_op == "READ":
                            cell = loop_arg % MAX_MEMORY
                            if input_idx < len(inputs):
                                memory[cell] = inputs[input_idx]
                                input_idx += 1
                            if len(stack) < MAX_STACK:
                                stack.append(memory[cell])
                        elif loop_op == "WRITE":
                            cell = loop_arg % MAX_MEMORY
                            if stack:
                                memory[cell] = stack[-1]
                                outputs.append(stack[-1])
                    pc += 1  # skip the looped instruction
            elif op == "READ":
                cell = arg % MAX_MEMORY
                if input_idx < len(inputs):
                    memory[cell] = inputs[input_idx]
                    input_idx += 1
                if len(stack) < MAX_STACK:
                    stack.append(memory[cell])
            elif op == "WRITE":
                cell = arg % MAX_MEMORY
                if stack:
                    memory[cell] = stack[-1]
                    outputs.append(stack[-1])

                        elif op == "STORE":
                cell = arg % 64
                if stack:
                    memory[cell] = stack[-1]
            pc += 1

        return {
            "outputs": outputs,
            "final_stack": stack[-5:] if stack else [],
            "steps": steps,
            "halted": pc >= n_instr or steps >= self.max_steps,
            "timed_out": steps >= self.max_steps
        }


def substrate_budget():
    """What was provided BEFORE discovery started."""
    return {
        "primitive_count": PRIMITIVE_COUNT,
        "primitives": PRIMITIVES,
        "representation": "integer stack + 64-cell memory",
        "control": "JZ (bounded jump) + LOOP (bounded repeat)",
        "max_stack": MAX_STACK,
        "max_memory": MAX_MEMORY,
        "max_steps": MAX_STEPS,
        "max_program_length": MAX_PROGRAM_LENGTH,
        "value_modulus": VALUE_MOD,
        "search": "NOT PROVIDED (external to substrate)",
        "heuristics": "NOT PROVIDED",
        "priors": "NOT PROVIDED",
        "external_knowledge": "NOT PROVIDED",
        "reasoning": "NOT PROVIDED",
        "planning": "NOT PROVIDED",
        "intelligence": "NOT PROVIDED",
        "creativity": "NOT PROVIDED",
        "abstraction": "NOT PROVIDED",
        "self_improvement": "NOT PROVIDED",
    }


def validate_substrate():
    """
    PHASE 0: Prove the substrate can compute.
    This MUST pass before discovery begins.
    """
    ex = Executor()
    results = {}

    # Test 1: Can it push and write a constant?
    p1 = Program([("PUSH", 0), ("WRITE", 0), ("HALT", 0)], constants=[42])
    r1 = ex.execute(p1, inputs=[])
    results["push_write"] = {
        "expected": [42],
        "actual": r1["outputs"],
        "pass": r1["outputs"] == [42]
    }

    # Test 2: Can it add two constants?
    p2 = Program([("PUSH", 0), ("PUSH", 1), ("ADD", 0), ("WRITE", 0), ("HALT", 0)], constants=[3, 7])
    r2 = ex.execute(p2, inputs=[])
    results["add_constants"] = {
        "expected": [10],
        "actual": r2["outputs"],
        "pass": r2["outputs"] == [10]
    }

    # Test 3: Can it read inputs and sum them?
    p3 = Program([
        ("READ", 0), ("READ", 1), ("ADD", 0), ("WRITE", 2), ("HALT", 0)
    ], constants=[])
    r3 = ex.execute(p3, inputs=[5, 3])
    results["read_add_write"] = {
        "expected": [8],
        "actual": r3["outputs"],
        "pass": r3["outputs"] == [8]
    }

    # Test 4: Can it compare?
    p4 = Program([
        ("PUSH", 0), ("PUSH", 1), ("GT", 0), ("WRITE", 0), ("HALT", 0)
    ], constants=[10, 3])
    r4 = ex.execute(p4, inputs=[])
    results["compare_gt"] = {
        "expected": [1],
        "actual": r4["outputs"],
        "pass": r4["outputs"] == [1]
    }

    # Test 5: Can it do conditional jump?
    p5 = Program([
        ("PUSH", 0), ("JZ", 4), ("PUSH", 1), ("WRITE", 0), ("HALT", 0),
        ("PUSH", 2), ("WRITE", 0), ("HALT", 0)
    ], constants=[0, 99, 77])
    r5 = ex.execute(p5, inputs=[])
    results["conditional_jz"] = {
        "expected": [77],
        "actual": r5["outputs"],
        "pass": r5["outputs"] == [77]
    }

    # Test 6: Sum 3 inputs
    p6 = Program([
        ("READ", 0), ("READ", 1), ("ADD", 0), ("READ", 2), ("ADD", 0), ("WRITE", 3), ("HALT", 0)
    ], constants=[])
    r6 = ex.execute(p6, inputs=[1, 2, 3])
    results["sum_3_inputs"] = {
        "expected": [6],
        "actual": r6["outputs"],
        "pass": r6["outputs"] == [6]
    }

    # Summary
    all_pass = all(r["pass"] for r in results.values())
    results["ALL_PASS"] = all_pass

    return results


if __name__ == "__main__":
    print("SUBSTRATE VALIDATION")
    print("=" * 50)
    results = validate_substrate()
    for name, r in results.items():
        if name == "ALL_PASS":
            print(f"\n  ALL PASS: {r}")
        else:
            status = "PASS" if r["pass"] else "FAIL"
            print(f"  [{status}] {name}: expected={r['expected']} actual={r['actual']}")
    print("\n" + json.dumps(substrate_budget(), indent=2))
