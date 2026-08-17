# ACID ADVERSARIAL AUDIT RESULTS

## Date: 2026-08-16

## Protocol
Blind adversarial scientific audit.
Objective: Find counterexamples. No goalpost shifting.

## TEST RESULTS

### TEST E: MODULO HONESTY
- Integer arithmetic: FAILED (501/1000)
- Modular arithmetic: PROVEN (1000/1000)
- COUNTEREXAMPLE: Negative sums wrap around

### TEST D: ANTI-OVERFITTING
- 93/93 overfit candidates rejected
- 0 verifier failures
- STATUS: PROVEN UNDER PROTOCOL

### TEST A: TRUE GENERALIZATION
- 10/10 tasks, 1000/1000 held-out each
- STATUS: PROVEN UNDER PROTOCOL (positive domain)

### TEST B: KNOWLEDGE TRANSFER CAUSALITY
- B (real): 100% success, 30 evals
- A (none): 40% success, 2389 evals
- C (random): 37% success
- D (shuffled): 30% success
- E (wrong-task): 40% success
- Effect size: 3.62
- STATUS: PROVEN UNDER PROTOCOL

### TEST C: ARTIFACT IS NOT THE ANSWER
- Original: 100% success
- Shuffled: 70% success
- Random: 0% success
- Truncated: 70% success
- Corrupt 10%: 50% success
- Corrupt 25%: 30% success
- Artifact solves sum4 directly: NO
- STATUS: PROVEN UNDER PROTOCOL

### TEST F: BLIND UNSEEN TASK
- 10000/10000 held-out correct
- STATUS: PROVEN UNDER PROTOCOL

### TEST G: SELF-IMPROVEMENT CUMULATIVE
- Improvement detected but not monotonic
- KB grows 0 -> 2
- STATUS: SUPPORTED

### TEST H: ABLATION
- artifact: NECESSARY
- mutation: NOT NECESSARY
- selection: NECESSARY
- verification: NOT NECESSARY

### TEST I: REPRODUCIBILITY
- 3/3 runs identical
- STATUS: PROVEN UNDER PROTOCOL

### TEST J: KILL TEST
- COUNTEREXAMPLES FOUND: 2
  - seed_sensitivity (1/10 seeds)
  - modulo_assumption (negative sums wrap)

## CAUSALITY CHALLENGE RESULTS

### CRITICAL FINDING
THE ARTIFACT IS EXACTLY THE SOLUTION.
artifact_sum4_extended == sum4_solution (identical).
THIS IS RETRIEVAL, NOT TRANSFER.

### MINIMAL SYSTEM TEST (100 seeds)
condition | success | mean_evals
A (full)  | 1.0     | 30
B (no art)| 0.41    | 2323.8
C (no mut)| 1.0     | 30
D (no sel)| 0.3     | 2531.7
E (no ver)| 1.0     | 30
F (random)| 0.32    | 2500.8
G (brute) | 1.0     | 1

### MUTATION RATE SWEEP
0% mutation: 100% success
50% mutation: 100% success
MUTATION IS NOT A CAUSAL COMPONENT

### SEED SENSITIVITY (100 seeds)
NO ARTIFACT: 41/100 success
REAL ARTIFACT: 100/100 success
DIFFERENCE: 59 percentage points
STATISTICALLY SIGNIFICANT

### RANDOM SEARCH BASELINE
ACID search (no artifact): 41% success
Random search: 32% success
Difference: 9 percentage points

### BLIND GENERALIZATION (10 tasks)
10/10 tasks: 10000/10000 each
TOTAL: 100000/100000
AGGREGATE: 100.0%

### NEGATIVE DOMAIN
10000/10000 correct with negative inputs
MODULAR ARITHMETIC CAPABILITY PROVEN

## CAUSAL MECHANISM IDENTIFIED

The artifact IS the causal mechanism.
The search provides a marginal 9pp improvement over random.
Mutation, verification, and transfer are not causal.

WHEN THE ARTIFACT IS THE ANSWER:
THIS IS RETRIEVAL, NOT DISCOVERY.

## FINAL CAPABILITY TABLE

CAPABILITY                  STATUS
------------------------------------------------
Program synthesis           SUPPORTED (with artifact)
Positive-domain solving     PROVEN
Modular arithmetic          PROVEN
Integer arithmetic          FAILED
Transfer                    NOT PROVEN (artifact = answer)
Self-improvement            NOT PROVEN
Mutation contribution       NOT PROVEN
Selection contribution      SUPPORTED (9pp over random)
Verification contribution   NOT PROVEN
Blind generalization        PROVEN
Seed reliability            NOT PROVEN
Reproducibility             PROVEN
General intelligence        NOT TESTED

## THE HONEST ANSWER

WHAT PART OF ACID ACTUALLY CAUSES THE RESULT?

THE ARTIFACT.

Without the artifact:
- ACID search: 41% success
- Random search: 32% success
- Difference: 9 percentage points

The 9 percentage point difference is the actual contribution
of ACID's search mechanism (selection + mutation).

Everything else is the artifact.

## COUNTEREXAMPLES FOUND

1. MODULO ASSUMPTION
   Negative sums wrap around due to modulo arithmetic.
   CLAIM "integer arithmetic" = INVALIDATED.

2. SEED SENSITIVITY
   Only 1/10 random seeds find the solution without artifact.
   CLAIM "reliable discovery" = NOT PROVEN.

3. ARTIFACT = ANSWER
   The artifact for sum4 IS the sum4 solution.
   CLAIM "transfer" = INVALIDATED (this is retrieval).
