# ACID v17 Fix: Correct Max Program + Search Results

## Date: 2026-08-18

## KNOWN MAX SOLUTION: FIXED AND VERIFIED

The previous max_prog had a bug (JZ target pointed to H instead of false branch).
The fixed max_prog works perfectly:

- Manual trace: 4/4 PASS
- 100 random tests: 100/100
- 1000 held-out tests: 1000/1000
- 30 adversarial tests: 30/30 pass, 0 fail

The substrate CAN express conditional operations.
The known solution is correct and verified.

## SEARCH RESULTS

Evolutionary search with:
- Population: 100
- Generations: 500
- Candidates tested: 50000
- Best fit: 0.6 (6/10 discovery examples)

The search CANNOT achieve fit=1.0.
The search CANNOT discover conditional branching patterns.

This confirms: SEARCH DEPTH FOR CONDITIONAL PATTERNS is the boundary.

The search space for conditional patterns is enormous because:
1. JZ jump target must be exactly correct
2. Stack management must be correct for both branches
3. The program must have the right structure (ST/LD for saving inputs)
4. The search space grows exponentially with program length

## COMPOSITION RESULTS

max(x0,x1) + x2: 490/1000

The composition partially works but has a bug:
The JZ jump target in max_body is an absolute index.
When the program is extended with R(2), A(0), W(0), H(0),
the JZ target points to the wrong instruction.

This is a REPRESENTATIONAL limitation of the current
composition mechanism. Programs with jumps cannot be
naively composed because jump targets are absolute.

## KEY FINDINGS

### 1. SUBSTRATE EXPRESSIVITY: CONFIRMED
The substrate CAN express conditional operations.
The known max solution works perfectly (1000/1000).

### 2. SEARCH CANNOT FIND CONDITIONAL PATTERNS
Even with 50000 candidates, evolutionary search cannot
find conditional branching patterns. Best fit: 0.6.

### 3. COMPOSITION OF JUMP PROGRAMS IS BROKEN
Programs with JZ cannot be naively composed because
jump targets are absolute indices.

### 4. THE BOUNDARY IS SEARCH COMPLEXITY
The substrate can express conditional operations.
The search cannot find them.
This is a SEARCH COMPLEXITY limitation, not representational.

## CLAIMS TABLE

| Claim | Status |
|-------|--------|
| Known max solution (fixed) | PROVEN (1000/1000) |
| Independent falsification | PROVEN (30/30) |
| Conditional capability discovery | NOT PROVEN (fit=0.6) |
| Discovered program held-out | FAILED (0/1000) |
| Composition (max + add) | PARTIAL (490/1000) |
| Frontier expansion | NOT PROVEN |

## FAILURE ANALYSIS

The search cannot discover conditional patterns because:
1. The search space is enormous (exponential in program length)
2. JZ jump targets must be exactly correct
3. Stack management must be correct for both branches
4. The program must have the right structure (ST/LD)

The composition of jump programs is broken because:
1. JZ targets are absolute indices
2. Extending a program changes instruction indices
3. Jump targets point to wrong instructions after extension

## FINAL VERDICT

SUBSTRATE EXPRESSIVITY = PROVEN (conditional operations expressible)
SEARCH DISCOVERY OF CONDITIONAL PATTERNS = NOT PROVEN
COMPOSITION OF JUMP PROGRAMS = PARTIAL (490/1000)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
GENERAL INTELLIGENCE = NO

The boundary is SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.
The substrate CAN express conditional operations.
The search CANNOT find them.
Composition of jump programs requires jump target adjustment.

NEXT HIGHEST-INFORMATION EXPERIMENT:
  Implement jump target adjustment for composition.
  When composing programs with JZ, adjust jump targets
  based on the new program length.
  
  Alternatively: implement a specialized conditional-pattern
  search that explicitly tries GT/LT + JZ combinations
  with correct jump targets.
