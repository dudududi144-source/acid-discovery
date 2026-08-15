"""
ACID Substrate - Minimal computational substrate.
19 primitives: PUSH, POP, DUP, SWAP, ADD, SUB, MUL, MOD,
               GT, LT, EQ, AND, OR, NOT, JZ, READ, WRITE, STORE, HALT
"""
import hashlib
import json

PRIMITIVES = ["PUSH", "POP", "DUP", "SWAP", "ADD", "SUB", "MUL", "MOD",
              "GT", "LT", "EQ", "AND", "OR", "NOT", "JZ", "READ", "WRITE", "STORE", "LOAD", "HALT"]

MAX_STACK = 256
MAX_MEMORY = 64
MAX_STEPS = 10000
MAX_PROGRAM_LENGTH = 200


class SubstrateProgram:
    def __init__(self, instructions, constants=None):
        self.instructions = instructions
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


class Executor:
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
        n = len(instr)

        while pc < n and steps < self.max_steps:
            op = instr[pc][0]
            arg = instr[pc][1]
            steps += 1

            if op == "HALT":
                break
            elif op == "PUSH":
                if len(stack) < MAX_STACK:
                    stack.append(consts[arg % len(consts)] if consts else arg % 100)
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
                    stack.append((a + b) % 1000000)
            elif op == "SUB":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append((a - b) % 1000000)
            elif op == "MUL":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append((a * b) % 1000000)
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
                        target = arg % n
                        if 0 <= target < n:
                            pc = target
                            continue
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
                cell = arg % MAX_MEMORY
                if stack:
                    memory[cell] = stack[-1]
                elif op == "LOAD":
                    cell = arg % MAX_MEMORY
                    if len(stack) < MAX_STACK:
                        stack.append(memory[cell])

            pc += 1

        return {"outputs": outputs, "steps": steps, "halted": pc >= n or steps >= self.max_steps}


def validate_substrate():
    ex = Executor()
    results = {}
    tests = [
        ("push_write", [("PUSH", 0), ("WRITE", 1), ("HALT", 0)], [42], [], [42]),
        ("add", [("PUSH", 0), ("PUSH", 1), ("ADD", 0), ("WRITE", 2), ("HALT", 0)], [3, 7], [], [10]),
        ("read_add", [("READ", 0), ("READ", 1), ("ADD", 0), ("WRITE", 2), ("HALT", 0)], [], [2, 3], [5]),
        ("store", [("READ", 0), ("STORE", 1), ("HALT", 0)], [], [42], []),
    ]
    for name, instr, consts, inputs, expected in tests:
        prog = SubstrateProgram(instr, consts)
        result = ex.execute(prog, inputs=inputs)
        results[name] = {"pass": result["outputs"] == expected, "expected": expected, "actual": result["outputs"]}
    return results
