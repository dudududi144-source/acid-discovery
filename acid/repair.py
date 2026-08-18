"""
ACID Repair Engine - Diagnostic Mathematical Repair

Implements the general failure-to-capability loop:
  SEARCH -> PARTIAL -> DIAGNOSE -> INFER -> REPAIR -> VERIFY

Hypothesis types:
  - missing_operand_add: delta == input[k]
  - missing_operand_mul: ratio == input[k]  
  - wrong_operator: ADD <-> MUL replacement
  - missing_composition: multi-step insertion

NO HUMAN LABELS. NO TEMPLATES. NO TASK NAMES.
The system infers repairs from mathematical deltas.
"""

def execute(prog, inputs):
    """Execute a program on the fixed substrate."""
    s, m, o, ii = [], [0]*64, [], 0
    for op, a in prog[:60]:
        if op == "H": break
        elif op == "R":
            if ii < len(inputs): m[a%64] = inputs[ii]; ii += 1
            if len(s) < 256: s.append(m[a%64])
        elif op == "A" and len(s) >= 2: b, x = s.pop(), s.pop(); s.append((x+b)%1000000)
        elif op == "M" and len(s) >= 2: b, x = s.pop(), s.pop(); s.append((x*b)%1000000)
        elif op == "S" and len(s) >= 2: b, x = s.pop(), s.pop(); s.append((x-b)%1000000)
        elif op == "D" and s: s.append(s[-1])
        elif op == "W" and s: o.append(s[-1])
    return o


def generate_hypotheses(partial, tests, n_inputs):
    """
    Generate competing hypotheses about what is wrong with a partial program.
    No hardcoded delta rule. Tests multiple relationship types.
    
    Returns: (hypotheses, diagnostic_data)
    """
    hypotheses = []
    diag = []
    
    for inp, exp in tests:
        actual = execute(partial, inp)
        a_val = actual[0] if actual else 0
        diag.append({
            "input": inp, "expected": exp[0], "actual": a_val,
            "delta": (exp[0] - a_val) % 1000000,
            "ratio": exp[0] / a_val if a_val != 0 else None
        })
    
    # TYPE 1: Additive missing operand
    for k in range(n_inputs):
        matches = sum(1 for d in diag if d["delta"] == d["input"][k])
        if matches >= len(diag) - 1:
            hypotheses.append({
                "type": "missing_operand_add",
                "relation": "delta == input[" + str(k) + "]",
                "consistency": matches / len(diag),
                "repair": [("R", k), ("A", 0)],
                "edit": "insert"
            })
    
    # TYPE 2: Multiplicative missing operand
    for k in range(n_inputs):
        matches = sum(1 for d in diag if d["ratio"] is not None and abs(d["ratio"] - d["input"][k]) < 0.01)
        if matches >= len(diag) - 1 and matches > 0:
            hypotheses.append({
                "type": "missing_operand_mul",
                "relation": "expected/actual == input[" + str(k) + "]",
                "consistency": matches / len(diag),
                "repair": [("R", k), ("M", 0)],
                "edit": "insert"
            })
    
    # TYPE 3: Wrong operator
    has_add = any(op == "A" for op, _ in partial)
    has_mul = any(op == "M" for op, _ in partial)
    
    if has_add and not has_mul:
        test_prog = [(op if op != "A" else "M", a) for op, a in partial]
        matches = sum(1 for inp, exp in tests if execute(test_prog, inp) == exp)
        if matches >= len(tests) - 1:
            hypotheses.append({
                "type": "wrong_operator",
                "relation": "ADD should be MUL",
                "consistency": matches / len(tests),
                "repair": [("A", "M")],
                "edit": "replace"
            })
    
    if has_mul and not has_add:
        test_prog = [(op if op != "M" else "A", a) for op, a in partial]
        matches = sum(1 for inp, exp in tests if execute(test_prog, inp) == exp)
        if matches >= len(tests) - 1:
            hypotheses.append({
                "type": "wrong_operator",
                "relation": "MUL should be ADD",
                "consistency": matches / len(tests),
                "repair": [("M", "A")],
                "edit": "replace"
            })
    
    # TYPE 4: Missing composition
    for j in range(n_inputs):
        for k in range(n_inputs):
            if j == k: continue
            matches_add = sum(1 for d in diag if d["delta"] == (d["input"][j]+d["input"][k])%1000000)
            if matches_add >= len(diag) - 1:
                hypotheses.append({
                    "type": "missing_composition_add",
                    "relation": "delta == input[" + str(j) + "]+input[" + str(k) + "]",
                    "consistency": matches_add / len(diag),
                    "repair": [("R",j),("R",k),("A",0),("A",0)],
                    "edit": "insert"
                })
            matches_mul = sum(1 for d in diag if d["delta"] == (d["input"][j]*d["input"][k])%1000000)
            if matches_mul >= len(diag) - 1:
                hypotheses.append({
                    "type": "missing_composition_mul",
                    "relation": "delta == input[" + str(j) + "]*input[" + str(k) + "]",
                    "consistency": matches_mul / len(diag),
                    "repair": [("R",j),("R",k),("M",0),("A",0)],
                    "edit": "insert"
                })
    
    return hypotheses, diag


def apply_repair(partial, hypothesis):
    """Apply the minimal repair based on the selected hypothesis."""
    if hypothesis["edit"] == "insert":
        write_pos = len(partial)
        for i, (op, _) in enumerate(partial):
            if op == "W": write_pos = i; break
        return partial[:write_pos] + hypothesis["repair"] + partial[write_pos:]
    elif hypothesis["edit"] == "replace":
        old_op, new_op = hypothesis["repair"][0]
        return [(op if op != old_op else new_op, a) for op, a in partial]
    return partial


def repair_program(partial, tests, n_inputs):
    """
    Full repair pipeline:
      1. Generate hypotheses from diagnostic data
      2. Select best hypothesis by consistency
      3. Apply minimal repair
      4. Return repaired program + metadata
    """
    hypotheses, diag = generate_hypotheses(partial, tests, n_inputs)
    
    if not hypotheses:
        return None, {"status": "no_hypothesis", "diagnostic": diag}
    
    best = max(hypotheses, key=lambda h: h["consistency"])
    repaired = apply_repair(partial, best)
    
    return repaired, {
        "status": "repaired",
        "hypothesis": best,
        "diagnostic": diag,
        "all_hypotheses": hypotheses
    }
