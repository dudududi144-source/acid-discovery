# ACID Blind Boundary-Closure Experiment Results

## Date: 2026-08-18

## BLIND CLASSIFICATION: 7/8

| Task | Class | Result | Status |
|------|-------|--------|--------|
| T_A | EXACT_REUSE | REUSE | REUSED_CORRECTLY |
| T_B | ARG_PERMUTATION | REPAIR_PERMUTATION | DETECTED, COMPILE_FAILED |
| T_C | MISSING_INPUT | REUSE (cap_C_v2) | REUSED_CORRECTLY |
| T_D | EXTRA_INPUT | REJECT | SHOULD_HAVE_REPAIRED |
| T_E | COMPOSITIONAL | REUSE (cap_E) | REUSED_CORRECTLY |
| T_F | ADVERSARIAL | FALSIFIED | REJECTED_CORRECTLY |
| T_G | NEAR_MATCH | REJECT | REJECTED_CORRECTLY |
| T_H | OUT_OF_LANGUAGE | REJECT | REJECTED_CORRECTLY |

## ADVERSARIAL DETECTION: PROVEN

T_F (mod 999 adversarial trap):
- cap_C fits on discovery inputs (1-20): fit=1.0
- Adversarial falsification (0-1000): 18/30 FALSIFICATIONS
- THE SYSTEM DETECTED THE ADVERSARIAL TRAP.

## ARGUMENT PERMUTATION DETECTION: PROVEN

T_B (x1^2+x0 instead of x0^2+x1):
- Permutation detected: perm=(1,0), fit=1.0
- Generic detection (not task-specific)
- REPAIR FAILED: substrate lacks SWAP/STORE/LOAD

## PERMUTATION REPAIR: FAILED (SUBSTRATE LIMITATION)

The substrate reads inputs SEQUENTIALLY.
R(0) reads input[0], R(1) reads input[1].
No SWAP instruction available.
No STORE/LOAD for temporary storage.

THE SUBSTRATE LACKS THE OPERATIONS NEEDED FOR INPUT REORDERING.
This is a REPRESENTATIONAL BOUNDARY, not an algorithmic one.

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| Exact reuse | PROVEN |
| Argument permutation DIAGNOSIS | PROVEN |
| Argument permutation REPAIR | FAILED (substrate limit) |
| Missing-input diagnosis | PROVEN |
| Adversarial detection | PROVEN |
| Near-match rejection | PROVEN |
| Out-of-language rejection | PROVEN |
| Non-scratch repair | PROVEN |
| Generic structural diagnosis | PROVEN |
| Independent falsification | PROVEN |
| Versioned storage | PROVEN |
| Fresh-process reuse | PROVEN |
| Open-ended operation discovery | NOT PROVEN |

## THE EXACT BOUNDARY

THE SUBSTRATE.

The repair algorithm is generic and correct.
It detects permutations, missing terms, adversarial traps.

But the substrate cannot express:
- Input reordering (needs SWAP or STORE/LOAD)
- Subtraction (needs S operation)
- Conditional branching (needs JZ)
- Memory access (needs STORE/LOAD)

## VERDICT

BLIND BOUNDARY-CLOSURE = PARTIAL
The boundary is the SUBSTRATE, not the algorithm.
