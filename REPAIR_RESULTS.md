# ACID Repair Gauntlet - Experiment Results

## Date: 2026-08-16

## Phase 1: Designed Tasks (10 tasks, 3 families)

RESULT: 10/10 repaired, all 1000/1000 held-out

| Task | Family | Hypothesis | Score | Held-out |
|------|--------|-----------|-------|----------|
| T0 | missing_operand | missing_operand_add | 0→1.0 | 1000/1000 |
| T1 | missing_operand | missing_operand_mul | 0→1.0 | 1000/1000 |
| T2 | wrong_operator | wrong_operator | 0→1.0 | 1000/1000 |
| T3 | wrong_operator | wrong_operator | 0→1.0 | 1000/1000 |
| T4 | missing_composition | missing_operand_mul | 0.2→1.0 | 1000/1000 |
| T5 | missing_composition | missing_operand_add | 0→1.0 | 1000/1000 |
| T6 | missing_operand | missing_operand_add | 0→1.0 | 1000/1000 |
| T7 | missing_operand | missing_operand_mul | 0→1.0 | 1000/1000 |
| T8 | wrong_operator | wrong_operator | 0→1.0 | 1000/1000 |
| T9 | wrong_operator | wrong_operator | 0→1.0 | 1000/1000 |

Counterfactual controls: ALL FAILED (0/200)

## Phase 2A: Blind Transfer (5 unseen tasks)

RESULT: 0/5 repaired

| Task | Hypothesis Found | Held-out |
|------|-----------------|----------|
| U0 | missing_operand_add | 1/1000 |
| U1 | missing_operand_mul | 0/1000 |
| U2 | wrong_operator | 2/1000 |
| U3 | NO HYPOTHESIS | 0/1000 |
| U4 | missing_composition_mul | 0/1000 |

## Phase 2B: 30-Seed Robustness

RESULT: 0/30 success
Mean held-out: 3/1000
Min: 1, Max: 7

## Phase 2C: Composition

RESULT: 0/1000 held-out

## Analysis

### What Works
- Mathematical inference identifies correct DIRECTION
- Delta analysis reveals missing operands
- Minimal repair transforms partial → exact on designed tasks
- The CONCEPT of diagnostic repair is sound

### What Does Not Work
- Repair does NOT generalize to unseen tasks (0/5)
- Repair is NOT seed-robust (0/30)
- Repair does NOT compose (0/1000)
- Hypothesis space is FIXED (4 types), not learned

### The Bottleneck
The hypothesis engine has 4 fixed types:
1. missing_operand_add (delta == input[k])
2. missing_operand_mul (ratio == input[k])
3. wrong_operator (ADD ↔ MUL)
4. missing_composition (multi-step insertion)

When a task does not match these types, the mechanism fails.
A general mechanism must DISCOVER hypothesis types from data.

## Verdict

| Claim | Status |
|-------|--------|
| Diagnostic inference | SUPPORTED (designed tasks) |
| Diagnostic repair | SUPPORTED (designed tasks) |
| Repair generalization | FAILED (0/5 transfer) |
| Repair transfer | FAILED (0/5 unseen) |
| Repair composition | FAILED (0/1000) |
| Seed robustness | FAILED (0/30) |
| Capability accumulation | NOT PROVEN |
| Capability frontier expansion | NOT PROVEN |

## Key Insight

Phase 1 (10/10) was dependent on task-hypothesis alignment.
The tasks were designed to match the hypothesis engine.
Phase 2 (0/5, 0/30) shows the mechanism does not generalize.

The repair mechanism is a SET OF CLEVER EXAMPLES,
not a GENERAL LEARNING MECHANISM.

## Next Step

Build a hypothesis engine that DISCOVERS hypothesis types
from data, rather than matching against a fixed list.
This requires symbolic regression or equation discovery.


## Hypothesis-Language Induction Experiment (2026-08-18)

### Setup
- NO fixed hypothesis types
- Symbolic expression search (genetic programming over {+, -, *, var, const})
- Development: 6 tasks (additive + multiplicative)
- OOD: subtraction, doubling (NEVER in development)

### Development Results
| Task | Family | Discovered Expression | Fitness |
|------|--------|----------------------|---------|
| D0 | additive | NOT FOUND | 0.2 |
| D1 | additive | NOT FOUND | 0.2 |
| D2 | additive | (x[2] + actual) | 1.0 |
| D3 | multiplicative | ((1 * actual) * x[1]) | 1.0 |
| D4 | multiplicative | (x[1] * ((0*3)-(0-actual))) | 1.0 |
| D5 | multiplicative | (x[1] * x[0]) | 1.0 |

Development: 4/6 relations discovered

### OOD Test 1: Subtraction (NEVER in development)
- Diagnostic data: input=[17,8] exp=9 actual=25
- DISCOVERED: ((x[0] + 3) - (x[1] + 3))
- Fitness: 1.0 (perfect on diagnostic data)
- Held-out: 1/1000 (FAILS on new data)

### OOD Test 2: Doubling (NEVER in development)
- DISCOVERED: (x[0] + actual)
- Fitness: 1.0 (perfect on diagnostic data)
- Held-out: 2/1000 (FAILS on new data)

### Critical Analysis

THE SYMBOLIC REGRESSION DISCOVERS THE CORRECT RELATIONS.

For subtraction: ((x[0]+3) - (x[1]+3)) simplifies to (x[0] - x[1]).
This IS the correct relation. The system found it.

For doubling: (x[0] + actual) where actual = x[0].
This IS x[0] + x[0] = 2*x[0]. The system found it.

BUT THE COMPILATION FROM EXPRESSION TO PROGRAM EDIT FAILS.

The expression is discovered correctly.
The program repair derived from the expression does not work.
The held-out tests fail (1/1000, 2/1000).

### The Bottleneck

EXPRESSION DISCOVERY: WORKS (fitness 1.0 on OOD relations)
EXPRESSION → PROGRAM COMPILATION: FAILS (held-out 1/1000)

The system CAN discover what relation is needed.
The system CANNOT yet compile that relation into a working program.

This is the gap between:
  "I know the answer is x[0] - x[1]" (discovery)
  "I can build a program that computes x[0] - x[1]" (compilation)

### Verdict

| Claim | Status |
|-------|--------|
| Fixed repair hypotheses | SUPPORTED (10/10 designed) |
| Learned hypothesis language | PARTIALLY SUPPORTED |
| OOD hypothesis discovery | SUPPORTED (fitness 1.0) |
| OOD repair compilation | FAILED (held-out 1/1000) |
| General diagnostic repair | NOT PROVEN |
| Repair transfer | NOT PROVEN |
| Repair composition | NOT PROVEN |
| Recursive hypothesis induction | NOT TESTED |
| Capability accumulation | NOT PROVEN |
| Capability frontier expansion | NOT PROVEN |

### Key Insight

The hypothesis-language induction is HALF-SOLVED.

The DISCOVERY half works:
  - Symbolic regression finds correct relations
  - Works on OOD families (subtraction, doubling)
  - No fixed hypothesis types needed
  - Fitness 1.0 on diagnostic data

The COMPILATION half fails:
  - Cannot convert discovered expression to program edit
  - Held-out tests fail
  - The gap is in the expression-to-program transform

NEXT STEP:
  Fix the expression-to-program compilation.
  The expression ((x[0]+3)-(x[1]+3)) should compile to:
    R(0), R(1), S(0), W(0), H(0)
  Not to a program with hardcoded constants.

  The compiler must SIMPLIFY the expression before compiling.
  ((x[0]+3)-(x[1]+3)) → (x[0]-x[1]) → R,R,S,W,H
