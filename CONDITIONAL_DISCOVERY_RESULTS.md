# ACID v18: Jump Target Relocation + Conditional Search Results

## Date: 2026-08-18

## JUMP COMPOSITION: PROVEN (1000/1000)

The JZ target relocation fixed the composition bug.
max(x0,x1)+x2 now works perfectly:
- 100/100 discovery tests
- 1000/1000 held-out tests
- 30/30 adversarial tests
- 1000/1000 fresh-process reuse

Controls all fail correctly:
- max alone (wrong arity): 0/100
- add alone (wrong arity): 0/100
- random: 0/100

## COMPOSITION DEPTH 3: FAILED (493/1000)

(max(x0,x1)+x2)*x3: 493/1000
The depth 3 composition still has issues.
The JZ target relocation for depth 3 is more complex.
The false branch JZ target needs additional adjustment.

## CONDITIONAL DISCOVERY: NOT PROVEN

Specialized conditional search:
- max(x0,x1): fit=0.6 (same as evolutionary search)
- abs(x0-x1): fit=0.0 (template search failed)

The template-based search did NOT improve over evolutionary search.
The search still cannot find conditional patterns.

The boundary remains: SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.

## COMPARISON WITH v17.1

| Metric | v17.1 | v18 | Status |
|--------|-------|-----|--------|
| Composition max+x2 | 490/1000 | 1000/1000 | FIXED |
| Composition depth 3 | N/A | 493/1000 | FAILED |
| Conditional discovery (max) | fit=0.6 | fit=0.6 | NOT IMPROVED |
| Conditional discovery (abs) | N/A | fit=0.0 | NOT PROVEN |

## KEY FINDINGS

### 1. JUMP COMPOSITION IS NOW PROVEN
The JZ target relocation fixed the composition bug.
Programs with JZ can now be composed correctly at depth 2.

### 2. DEPTH 3 COMPOSITION STILL BROKEN
The depth 3 composition has a more complex JZ target issue.
The false branch JZ target needs additional adjustment
when the continuation code is longer.

### 3. CONDITIONAL DISCOVERY NOT IMPROVED
The specialized conditional search did NOT improve over
evolutionary search. The template-based approach did not
help discover conditional patterns.

The boundary remains: SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.

### 4. THE FUNDAMENTAL ISSUE
The search cannot find conditional patterns because:
1. The search space is enormous
2. JZ targets must be exactly correct
3. Stack management must be correct for both branches
4. The program must have the right structure (ST/LD)

Template-based search did not help because:
1. The templates still need correct JZ targets
2. The templates still need correct stack management
3. The search space is still enormous

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| Jump target relocation | PROVEN (1000/1000) |
| Composition depth 2 | PROVEN (1000/1000) |
| Composition depth 3 | FAILED (493/1000) |
| Conditional discovery (max) | NOT PROVEN (fit=0.6) |
| Conditional discovery (abs) | NOT PROVEN (fit=0.0) |
| Conditional discovery (min) | NOT TESTED |
| Conditional discovery (clamp) | NOT TESTED |
| Adversarial validation | PROVEN (30/30) |
| Fresh-process reuse | PROVEN (1000/1000) |
| Controls fail correctly | PROVEN |
| Open-ended operation discovery | NOT PROVEN |
| General intelligence | NO |

## FINAL VERDICT

JUMP COMPOSITION = PROVEN (1000/1000)
CONDITIONAL CAPABILITY DISCOVERY = NOT PROVEN
OPEN-ENDED CAPABILITY DISCOVERY = NOT PROVEN
GENERAL INTELLIGENCE = NO

The JZ target relocation fixed the composition bug.
Programs with JZ can now be composed at depth 2.
But conditional discovery remains NOT PROVEN.

The boundary is SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.
The substrate CAN express conditional operations.
The search CANNOT find them.
Template-based search did not improve discovery.

NEXT HIGHEST-INFORMATION EXPERIMENT:
  Fix depth 3 composition (JZ target for false branch).
  Implement a more sophisticated conditional search that
  explicitly constructs GT/LT + JZ patterns with correct
  jump targets and stack management.
