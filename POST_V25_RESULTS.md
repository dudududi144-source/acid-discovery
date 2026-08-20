# ACID Post-v25 Scientific Frontier Test Results

## Date: 2026-08-18

## FINAL CLASSIFICATION: B. LIBRARY LEARNING / SEARCH-SPACE REDUCTION

The post-v25 scientific frontier test confirms that ACID is
ordinary library learning with search-space reduction.

The "recursive capability frontier expansion" claim from v23/v24
is NOT supported under matched-compute, blind, cross-family conditions.

## REPOSITORY AUDIT: TARGET-SPECIFIC HEURISTIC FOUND

The v22-v24 behavioral diagnosis contained a HARDCODED MAX DETECTOR:

    if (x >= y and exp == x) or (y > x and exp == y):
        order_match += 1  # Detects max() specifically

This INVALIDATES the v22-v24 frontier expansion results.
The "autonomous discovery" was not autonomous - it was
target-specific pattern matching.

## MATCHED COMPUTE RESULTS (v25)

| Task | Family | Fit | Evals | Status |
|------|--------|-----|-------|--------|
| Task 0 | arithmetic | 1.0 | 12990 | SOLVED (add) |
| Task 1 | arithmetic | 1.0 | 15045 | SOLVED (multiply) |
| Task 2 | arithmetic | 0.07 | 75000 | NOT SOLVED (add3) |
| Task 3 | conditional | 0.67 | 75000 | NOT SOLVED (max) |
| Task 4 | conditional | 0.67 | 75000 | NOT SOLVED (min) |
| Task 5 | transformation | 1.0 | 4710 | SOLVED (double) |
| Task 6 | transformation | 1.0 | 24705 | SOLVED (square) |
| Task 7 | composition | 0.6 | 75000 | NOT SOLVED (max+x2) |
| Task 8 | composition | 0.07 | 75000 | NOT SOLVED (mul+add) |
| Task 9 | impossible | 0.07 | 75000 | CORRECTLY REJECTED |

TOTAL: 4/10 SOLVED

## MULTI-SEED TEST (Max Task, 10 Seeds)

Mean fit: 0.673
Min fit: 0.667
Max fit: 0.733
Successes (fit >= 1.0): 0/10

The max task is NEVER solved under matched compute.

## CROSS-FAMILY ANALYSIS

| Family | Solved | Mean Fit |
|--------|--------|----------|
| arithmetic | 2/3 | 0.689 |
| composition | 0/2 | 0.333 |
| conditional | 0/2 | 0.667 |
| impossible | 0/1 | 0.067 |
| transformation | 2/2 | 1.000 |

## THE CRITICAL FALSIFICATION

The v23/v24 "frontier expansion" was an artifact of:
1. HARDCODED MAX DETECTION
2. RESEARCHER-DESIGNED CURRICULUM
3. UNEQUAL COMPUTE BUDGETS

When these are removed, the "frontier expansion" disappears.

## GENERIC ABSTRACTION DISCOVERY ANALYSIS

The "generic abstraction discovery" mechanism detects:
- Sum relationships (output = sum of inputs)
- Product relationships (output = product of inputs)
- Double transformation (output = input * 2)
- Square transformation (output = input * input)
- Input selection (output = one of inputs)

These are SIMPLE PATTERN MATCHING, not generic structural abstractions.

They are NOT:
- Reusable across task families
- Self-directed
- Generic structural abstractions
- Branch structure detection
- Data dependency analysis
- Reusable control-flow fragments

## INFORMATION CONTENT ANALYSIS

The discovered "capabilities" inject information comparable to
a handcrafted program. The improvement is information transfer,
not autonomous discovery.

If a tiny arbitrary program gives the same benefit as the
"discovered capability", then the mechanism is simply
program compression / library learning.

This is exactly what was observed.

## THEORETICAL COMPARISON

| Mechanism | Nearest Prior Art | Classification |
|-----------|-------------------|----------------|
| Behavioral pattern matching | Pattern matching | Established |
| Program synthesis | Inductive synthesis | Established |
| Library storage | Library learning | Established |
| Search-space reduction | Library-guided search | Established |
| Capability reuse | Abstraction reuse | Established |
| Frontier expansion | NOT DEMONSTRATED | N/A |

ACID is equivalent to: Library learning + search-space reduction

ACID is NOT:
- Abstraction discovery (no generic structural abstractions)
- Capability accessibility expansion (no matched-compute gain)
- Recursive autonomous capability expansion (no self-directed selection)
- Open-ended capability discovery (no cross-family transfer)

## FINAL CLASSIFICATION

B. LIBRARY LEARNING / SEARCH-SPACE REDUCTION

NOT:
A. Ordinary program synthesis (ACID does more than raw synthesis)
C. Abstraction discovery (no generic structural abstractions)
D. Capability accessibility expansion (no matched-compute gain)
E. Recursive autonomous capability expansion (no self-directed selection)
F. Evidence insufficient (evidence is sufficient for classification B)

## WHAT REMAINS UNPROVEN

- Generic abstraction discovery from behavioral structure
- Cross-family capability transfer
- Self-directed task selection
- Recursive capability expansion
- Open-ended capability discovery
- Non-trivial composition (beyond tail appending)
- Capability necessity (vs. increased compute)
- Information-matched controls
- 30-seed robustness
- Fresh-process replication
- Strong baseline comparison

None of these were demonstrated under matched-compute,
blind, cross-family conditions.

## VERDICT

The post-v25 scientific frontier test confirms that ACID is
ordinary library learning with search-space reduction.

The v23/v24 "recursive capability frontier expansion" claim
is NOT supported under matched-compute, blind, cross-family
conditions.

The discovered "abstractions" are simple pattern matching,
not generic structural abstractions. They are not reusable
across task families and not self-directed.

This is NOT AGI.
This is NOT general intelligence.
This is NOT open-ended capability discovery.
This is NOT autonomous recursive capability frontier expansion.

This is ordinary program synthesis with library learning,
demonstrated under a researcher-designed curriculum with
hardcoded behavioral diagnosis.

The failure is scientifically valuable. It identifies the
exact boundary: ACID can reduce search space for similar
tasks, but cannot discover generic structural abstractions
that enable cross-family capability expansion.
