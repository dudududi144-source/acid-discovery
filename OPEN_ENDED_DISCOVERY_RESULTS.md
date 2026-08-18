# ACID Open-Ended Operation Discovery Results

## Date: 2026-08-18

## INITIAL LANGUAGE L0 (FROZEN)

L0 = {id(x), square(x), add(x,y)}
NOT in L0: sub, mul, max, abs, mod, conditional
L0 FROZEN before discovery.

## ANTI-CHEATING AUDIT: ALL PASS

All 10 anti-cheating checks passed.
No target-specific templates, hardcoded solutions, or leakage.

## LANGUAGE INSUFFICIENCY DETECTION: PROVEN

All 6 OOD tasks correctly identified as LANGUAGE_INSUFFICIENCY=True.
L0 cannot express any of the target operations.

## DISCOVERY RESULTS

| Task | Name | Discovered | Fit | Falsification | Held-out | Case |
|------|------|-----------|-----|---------------|----------|------|
| T1 | subtraction | YES | 1.0 | 30/30 VERIFIED | 1000/1000 | CASE_4_SUBSTRATE_DERIVED |
| T2 | multiplication | NO | 0.12 | N/A | N/A | CASE_4_SUBSTRATE_DERIVED |
| T3 | max | NO | 0.62 | N/A | N/A | CASE_3_REQUIRES_COMPOSITION |
| T4 | abs_diff | NO | 0.62 | N/A | N/A | CASE_3_REQUIRES_COMPOSITION |
| T5 | modulo | YES | 1.0 | 30/30 VERIFIED | 1000/1000 | CASE_4_SUBSTRATE_DERIVED |
| T6 | exponentiation | NO | N/A | N/A | N/A | IMPOSSIBLE (correctly rejected) |

Discovered: 2/6
Verified (1000/1000): 2/6
Transfer (cap_T1 + id): 1000/1000
Composition: 0/1000 (cap_T2 not discovered)
Negative control: CORRECTLY REJECTED

## CRITICAL FINDINGS

### 1. SUBSTRATE-DERIVED CONSTRUCT DISCOVERY: SUPPORTED

The system discovered subtraction (T1) and modulo (T5)
from behavioral evidence alone, using substrate primitives
S and MD that were NOT in L0.

These are CASE_4: the substrate already contains the primitive.
The system discovered a CONSTRUCT using the primitive.
This is NOT unrestricted open-ended discovery.

### 2. SEARCH EFFICIENCY LIMITATION

T2 (multiplication) was NOT discovered despite M being
in the substrate. The random search over 500 candidates
did not find the 5-operation program R(0),R(1),M,W,H.

This is a SEARCH EFFICIENCY problem, not a representational one.
The substrate CAN express multiplication.
The random search is too weak to find it reliably.

### 3. COMPOSITION DISCOVERY: FAILED

T3 (max) and T4 (abs_diff) require multi-step programs
with conditional branching. The random search found
partial solutions (fit=0.62) but not complete ones.

These are CASE_3: genuine composition discovery.
The system CANNOT discover these with random search.

### 4. IMPOSSIBLE TASK: CORRECTLY REJECTED

T6 (exponentiation) requires an operation NOT in the substrate.
The system correctly rejected it.
REPRESENTATIONAL_INSUFFICIENCY detected.

### 5. BLIND TRANSFER: PROVEN

cap_T1 (subtraction) was composed with id(x) to solve
x0-x1+x2. Held-out: 1000/1000.

## CLASSIFICATION OF DISCOVERED CONSTRUCTS

T1 (subtraction):  CASE_4_SUBSTRATE_DERIVED (S in substrate)
T2 (multiplication): CASE_4_SUBSTRATE_DERIVED (M in substrate, NOT DISCOVERED)
T3 (max):          CASE_3_REQUIRES_COMPOSITION (NOT DISCOVERED)
T4 (abs_diff):     CASE_3_REQUIRES_COMPOSITION (NOT DISCOVERED)
T5 (modulo):       CASE_4_SUBSTRATE_DERIVED (MD in substrate)
T6 (exponentiation): IMPOSSIBLE (correctly rejected)

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| L0 language insufficiency detection | PROVEN |
| Substrate-derived construct discovery | SUPPORTED (2/6) |
| Genuine new operation discovery (CASE_3) | NOT PROVEN |
| Independent falsification | PROVEN (30/30) |
| Held-out verification | PROVEN (1000/1000 for discovered) |
| Persistence | SUPPORTED (2 capabilities) |
| Blind transfer | PROVEN (1000/1000) |
| Composition | FAILED (cap_T2 not discovered) |
| Negative control (impossible task) | PROVEN (correctly rejected) |
| Multi-seed robustness | NOT TESTED |
| Blind replication | NOT TESTED |
| Open-ended operation discovery | NOT PROVEN |

## EXACT BOUNDARY

THE SUBSTRATE IS THE BOUNDARY.

The system can discover constructs expressible in the
20-primitive substrate. It CANNOT go beyond the substrate.

WITHIN the substrate:
  - Simple constructs (1-2 primitives): DISCOVERABLE
  - Complex compositions (3+ primitives): NOT DISCOVERABLE
    with random search (search efficiency limitation)
  - Impossible operations: CORRECTLY REJECTED

THE SEARCH EFFICIENCY LIMITATION:
  Random search over 500 candidates found 2/4 substrate-
  derivable constructs. The search is too weak for
  reliable discovery of all substrate-expressible constructs.

NEXT HIGHEST-INFORMATION EXPERIMENT:
  Improve search efficiency (evolutionary search instead of
  random) and test whether CASE_3 constructs (max, abs)
  can be discovered with better search.

## FINAL VERDICT

SUBSTRATE-DERIVED CONSTRUCT DISCOVERY = SUPPORTED (2/6)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
CAPABILITY LANGUAGE EXTENSION = PARTIAL

The system extends its capability language WITHIN
the substrate's expressivity. It cannot extend
BEYOND the substrate.

This is not AGI. This is not superintelligence.
This is substrate-bounded construct discovery
with a search efficiency limitation.
