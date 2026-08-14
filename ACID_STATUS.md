# ACID STATUS - STATISTICAL COMPARISON COMPLETE

## Verdict: REFUTED (for sum_3)

Blocks do NOT improve discovery for sum_3.
Random search finds sum_3 in 10/10 seeds.
The task is too easy for blocks to matter.

## Exact Numbers

| Config | Found | Avg Evals | Std Dev | Speedup |
|--------|-------|-----------|---------|----------|
| Random | 10/10 | 2,697 | 3,148 | baseline |
| RPA | 10/10 | 3,260 | 3,204 | 0.83x (SLOWER) |
| RPA+WO | 10/10 | 2,554 | 3,630 | 1.06x (marginal) |

## Why This Is The Truth

1. sum_3 requires: READ+READ+ADD+READ+ADD+WRITE+HALT (7 ops)
2. With 500 gens x pop 50 = 25,000 evaluations per seed
3. Random mutation hits this 7-op pattern reliably
4. Blocks add structure but the search budget is already sufficient
5. Therefore: blocks provide no advantage for this task

## What This Means

The ACID system correctly reports a NEGATIVE result.
This is the system working as designed.
Truth > Appearance. Evidence > Claim.

## What Would Change The Result

To demonstrate block value, need:
1. Harder tasks (sum_10, sum_20, nested patterns)
2. Reduced search budget (50 gens, pop 10)
3. Tasks requiring 20+ specific instructions
4. Tasks where random search FAILS

## Cumulative ACID Findings

| Claim | Status | Evidence |
|-------|--------|----------|
| Substrate computes | CONFIRMED | 6/6 tests pass |
| Tasks require structure | CONFIRMED | random < 5% (calibrated) |
| Composition works | CONFIRMED | 3/4 seeds compose |
| Transfer works | CONFIRMED | sum_4 + sum_5 pass |
| Blocks speed up easy tasks | REFUTED | 0.83x-1.06x, no advantage |
| Self-improvement (easy tasks) | REFUTED | No speed gain |
| Self-improvement (hard tasks) | UNTESTED | Need harder tasks |
