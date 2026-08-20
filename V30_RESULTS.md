# ACID v30: Research Reset Results

## Date: 2026-08-18

## NULL HYPOTHESIS

H0: ACID provides no capability beyond ordinary program synthesis
with evolutionary search.

## COMPUTE EFFICIENCY CURVES

| Budget | ACID | BF | Diff |
|--------|------|-----|------|
| 500 | 0.056 | 0.167 | -0.111 |
| 1000 | 0.278 | 0.222 | +0.056 |
| 2000 | 0.333 | 0.278 | +0.056 |
| 5000 | 0.389 | 0.333 | +0.056 |

## ANALYSIS

Budgets where ACID > BF: 3/4
Budgets where BF > ACID: 1/4 (lowest budget)
Budgets where ACID == BF: 0/4

The advantage is SMALL (0.056) and consistent.
At low budget (500), BF actually wins.

## KEY FINDING

ACID shows a MARGINAL compute efficiency advantage at higher budgets,
but NOT at low budgets. This suggests that the evolutionary search
provides a small benefit when given enough compute, but doesn't help
when compute is very limited.

The advantage is approximately 1 task out of 18 (6 tasks x 3 seeds).
This is a very weak signal.

## CONCLUSION

H0 MAY BE REJECTED: ACID shows compute efficiency advantage.
But the advantage is very small and needs replication.

LEVEL: LEVEL 1: General search-efficiency improvement (pending replication)

NOT LEVEL 2 (reusable structural abstraction).
NOT LEVEL 3 (cross-family transfer).
NOT LEVEL 4 (open-ended discovery).

## RELEASE VERDICT: NO (pending replication)

The advantage is very small (0.056).
Only 3 seeds were used (not 20+).
Only 6 tasks were used (not enough for statistical significance).
The advantage disappears at low budget.

## WHAT WOULD BE NEEDED TO UPGRADE THE CLAIM

1. 20+ seeds (currently only 3)
2. 20+ tasks (currently only 6)
3. Statistical significance test
4. Adversarial testing
5. Cross-family transfer test
6. Compute efficiency advantage at ALL budgets

If all of these are satisfied, the claim could be upgraded to:
  LEVEL 1: General search-efficiency improvement (PROVEN)

But NOT to:
  LEVEL 2: Reusable structural abstraction
  LEVEL 3: Cross-family transfer
  LEVEL 4: Open-ended discovery

## COMPLETE PROJECT HISTORY (v22-v30)

v22: Conditional composition PROVEN (but hardcoded max detection)
v23: Recursive frontier expansion PROVEN (but researcher curriculum)
v24: Adversarial audit found methodological problems
v25: Matched compute: 4/10 solved
v26: Brutal red-team: 5/12 solved, RELEASE VERDICT: NO
v27: Generalization: 1/6 weak signal
v28: Prove the signal: 3/24 replicates (non-robust)
v29: Explain the advantage: CONCLUSION D - signal disappears
v30: Research reset: MARGINAL compute efficiency advantage (pending replication)

## FINAL ASSESSMENT

ACID shows a potential compute efficiency advantage.
The advantage is very small (0.056) and only at higher budgets.
At low budget (500), BF actually wins.

The current conclusion stands:
  ACID is ordinary program synthesis with evolutionary search,
  with a marginal compute efficiency advantage at higher budgets.

This is NOT capability discovery.
This is NOT frontier expansion.
This is NOT open-ended discovery.

The project has produced rigorous negative results.
These are scientifically valuable.
