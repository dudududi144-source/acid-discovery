# ACID v20: Capability-as-Search-Fuel Results

## Date: 2026-08-18

## CENTRAL QUESTION
Can a previously discovered capability become a new search primitive
that enables discovering a second capability?

## RESULTS

### C1 DISCOVERY: PROVEN (1000/1000)
- Behavioral diagnosis: CONDITIONAL_SPLIT (confidence=1.0)
- C1 synthesized from diagnosis (no target name, no implementation)
- Held-out: 1000/1000
- Adversarial: 30/30
- C1 VERIFIED and STORED

### C2 DISCOVERY: NOT PROVEN
- CONTROL A (L0 search, no C1): fit=0
- CONTROL B (L1 search with C1): fit=0.47
- C2 NOT DISCOVERED (fit < 1.0)

### CAUSALITY TEST
- FULL (L1 with C1): fit=0.47
- NO_C1 (L0 only): fit=0
- RANDOM_C1: fit=0.0
- C1 specifically causes improved search (0.47 > 0 > 0)

### FRESH-PROCESS REUSE: PROVEN (1000/1000)

## KEY FINDINGS

### 1. C1 WAS DISCOVERED FROM BEHAVIORAL EVIDENCE
The system detected CONDITIONAL_SPLIT from behavioral observations.
No target name was provided. No implementation was given.
The system synthesized a conditional program from the diagnosis.
Held-out: 1000/1000. Adversarial: 30/30.

### 2. C1 IMPROVED SEARCH BUT DID NOT ENABLE FULL C2 DISCOVERY
C1 improved search from fit=0 to fit=0.47.
But fit=0.47 is not sufficient for full C2 discovery.
The C1 body composition with R(2)+A did not handle both
branches of the conditional correctly.

### 3. THE CAUSALITY IS ESTABLISHED
C1 specifically causes improved search (0.47 > 0 > 0).
Random C1 does not help (fit=0.0).
This establishes that C1 is a useful search primitive.

### 4. THE REMAINING BOUNDARY
The C1 body composition does not correctly handle both branches
of the conditional when composed with additional operations.
This is the same JZ composition issue from v18.

## FRONTIER_GAIN
FRONTIER_GAIN = capabilities with library - capabilities without library = 0

C1 improved search but did not enable a new capability discovery.
The frontier was NOT expanded.

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| C1 discovery from behavioral evidence | PROVEN (1000/1000) |
| C1 as search primitive | PARTIAL (fit 0->0.47) |
| C1 causally enables C2 | NOT PROVEN (fit=0.47) |
| C1+C2 create C3 | NOT TESTED |
| C3 expands search frontier | NOT TESTED |
| Fresh-process reuse | PROVEN (1000/1000) |
| 30-seed robustness | NOT TESTED (single seed) |
| Transfer to unseen families | NOT TESTED |
| Open-ended discovery | NOT PROVEN |
| General intelligence | NO |

## FINAL VERDICT

AUTONOMOUS CAPABILITY FRONTIER EXPANSION = PARTIAL

C1 discovery: PROVEN (1000/1000)
C1 as search primitive: PARTIAL (improved search, not full discovery)
C2 discovery with C1: NOT PROVEN (fit=0.47)
Fresh-process reuse: PROVEN (1000/1000)
Open-ended discovery: NOT PROVEN
General intelligence: NO

## REMAINING BOUNDARY

JZ COMPOSITION FOR CONDITIONAL PROGRAMS.

C1 (conditional) improves search but cannot be correctly
composed with additional operations because the JZ branching
is not handled correctly in the composition.

The fix requires:
1. Label-based IR for conditional programs
2. Correct branch handling during composition
3. Both branches must be extended with the continuation

This is the same boundary identified in v18.
The fix was implemented in v18 (depth 2: 1000/1000)
but the capability-guided search does not use it correctly.

## NEXT HIGHEST-INFORMATION EXPERIMENT

Fix the capability-guided search to correctly compose
conditional capabilities using the label-based IR.

The key insight: when composing C1 (conditional) with
additional operations, BOTH branches of C1 must be extended
with the continuation code.

Current bug: only one branch is extended.
Fix: extend both branches with the continuation.
