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
