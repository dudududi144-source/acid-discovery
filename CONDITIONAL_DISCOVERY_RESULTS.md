# ACID v17: Capability-Guided Conditional Discovery Results

## Date: 2026-08-18

## CRITICAL FINDING: KNOWN SOLUTION WAS INCORRECT

The known max_prog solution achieved 0/100 on discovery tests
and 0/1000 on held-out tests. This means the known solution
was INCORRECT - a bug in the manually written program.

The search algorithms achieved fit=0.6, which is BETTER than
the known solution's 0.0.

## SEARCH RESULTS

| System | Fit | Candidates |
|--------|-----|-----------|
| A (random) | 0.6 | 1000 |
| B (evolutionary) | 0.6 | 10000 |
| D (cap-guided) | 0.6 | 500 |
| Known solution | 0.0 | N/A |

All three search systems achieved the same fit (0.6).
None could achieve fit=1.0.
The known solution was completely wrong (0.0).

## KEY FINDINGS

### 1. KNOWN SOLUTION BUG
The manually written max_prog was incorrect.
The JZ jump target was wrong (pointed to H instead of false branch).
The stack management was incorrect for both branches.

### 2. SEARCH ACHIEVED PARTIAL SUCCESS
All three search systems achieved fit=0.6.
This means they found programs that work on 60% of discovery examples.
But they could NOT achieve 100% fit.

### 3. CAPABILITY-GUIDED SEARCH DID NOT OUTPERFORM
D (capability-guided) achieved the same fit as A and B.
The hypothesis "capability-guided > raw search" is NOT SUPPORTED.

### 4. SEARCH DEPTH FOR CONDITIONAL PATTERNS
The boundary is SEARCH DEPTH FOR CONDITIONAL PATTERNS.
Conditional patterns require:
- GT/LT comparison
- JZ jump with correct target
- Branching structure
- Correct stack management for both branches

The search space for these patterns is enormous.
None of the search algorithms could find them in the allocated budget.

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| Known solution verification | FAILED (0/100, bug in known solution) |
| Independent falsification | FAILED (known solution was wrong) |
| Capability-guided > random search | NOT PROVEN (same fit) |
| Capability-guided > evolutionary search | NOT PROVEN (same fit) |
| Conditional capability discovery | NOT PROVEN (best fit=0.6) |
| Frontier expansion | NOT PROVEN |
| Multi-seed robustness | NOT TESTED (single seed) |
| Blind replication | NOT TESTED |
| Open-ended operation discovery | NOT PROVEN |

## FAILURE ANALYSIS

The search algorithms could NOT discover the conditional
branching pattern for max.

The boundary is SEARCH DEPTH FOR CONDITIONAL PATTERNS.

Conditional patterns require:
- GT/LT comparison
- JZ jump with correct target
- Branching structure
- Correct stack management

The search space for these patterns is enormous.
Random/evolutionary/capability-guided search cannot
find them in the allocated budget.

This is a SEARCH COMPLEXITY limitation,
not a representational limitation.

The substrate CAN express conditional operations.
The search CANNOT find them.

## FINAL VERDICT

CAPABILITY-GUIDED CONDITIONAL DISCOVERY = NOT PROVEN
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN

The hypothesis "capability-guided search > raw search"
is NOT SUPPORTED for conditional patterns.

All three search systems achieved the same fit (0.6).
None could discover conditional branching patterns.

The boundary is SEARCH DEPTH FOR CONDITIONAL PATTERNS.
This is a fundamental search complexity limitation.

NEXT HIGHEST-INFORMATION EXPERIMENT:
  Fix the known max_prog solution.
  Verify it achieves 1000/1000.
  Then test whether search can find it with larger budget.
  
  Alternatively: implement a specialized conditional-pattern
  search that explicitly tries GT/LT + JZ combinations.
  This would test whether the search space can be reduced
  by focusing on conditional patterns.
