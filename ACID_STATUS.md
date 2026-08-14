# ACID STATUS - HARD TASK ANALYSIS

## Latest Verdict: REFUTED (sum_6 also too easy for evolution)

## The Critical Finding

sum_6 is HARD for single random programs (0/1000).
sum_6 is EASY for evolutionary search (5/5 in 500 gens).

Evolutionary search accumulates partial solutions through selection.
After 500 generations, the full 12-op solution emerges.
Blocks provide no advantage because evolution already succeeds.

## Results

| Config | Found | Avg Evals | Note |
|--------|-------|-----------|------|
| Random | 5/5 | 6,671 | Evolution finds it |
| RPA | 4/5 | 7,325 | WORSE than random |
| RPA+RPA | 5/5 | 4,757 | Similar to random |

## The Real Question

To demonstrate block value, we need tasks where:
1. Single random programs fail (0/1000) - ACHIEVED
2. Evolutionary search ALSO fails - NOT YET ACHIEVED

sum_6 satisfies (1) but not (2).
Evolution with 500 gens still finds it.

## Next Steps

Option A: Reduce search budget (50 gens, pop 10)
Option B: Use sum_10 or sum_20 (20-40+ ops)
Option C: Tasks with no fitness gradient (all-or-nothing)
Option D: Accept that evolution is powerful and blocks help only at extreme difficulty

## Cumulative ACID Findings

| Claim | Status |
|-------|--------|
| Substrate computes | CONFIRMED |
| Composition works | CONFIRMED |
| Transfer works | CONFIRMED |
| Blocks help easy tasks | REFUTED |
| Blocks help medium tasks | REFUTED |
| Blocks help hard tasks (evolution fails) | UNTESTED |
| Evolution is more powerful than expected | CONFIRMED |
