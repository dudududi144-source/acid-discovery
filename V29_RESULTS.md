# ACID v29: Explain the Advantage Results

## Date: 2026-08-18

## CRITICAL FINDING: THE v28 SIGNAL DISAPPEARS UNDER STRONGER CONTROLS

In v28, ACID (evolutionary search) solved 3/24 nested_composition tasks.
In v29, evolutionary search (B2) solved 0/12 nested_composition tasks.

The difference: v28 and v29 used DIFFERENT task instances.

This means the v28 result was NOT robust.
It depended on specific task instances that happened to be
easier for evolutionary search.

## RESULTS

| System | Solved | Mean Fit |
|--------|--------|----------|
| B0 (Brute force) | 0/12 | 0.044-0.067 |
| B2 (Evolutionary) | 0/12 | 0.0-0.044 |

Difference: 0

## MECHANISM ANALYSIS

Hypothesis tested: The advantage comes from preserving partial solutions.

Result: B2 == B0 (both 0/12)

The advantage is NOT from preserving partial solutions.
The v28 result was due to specific task instances.

## CONCLUSION D: THE 3/24 SIGNAL DISAPPEARS UNDER STRONGER CONTROLS

The v28 result (3/24) was NOT robust.
It depended on specific task instances that happened to be
easier for evolutionary search.

When the task instances change, the advantage disappears.

This is CONCLUSION D: "The 3/24 signal disappears under stronger controls."

## IMPLICATION

The v28 result should be downgraded from:
  "ACID demonstrates meaningful advantage over ordinary search"
to:
  "ACID showed a non-robust signal that disappears under replication"

The v28 result was likely due to:
  - Specific task instances that happened to be easier
  - Stochastic variance
  - Benchmark-specific alignment

NOT due to:
  - Generic abstraction discovery
  - Evolutionary search bias
  - Reusable structural abstraction
  - Cross-family transfer

## LEVEL

LEVEL 0: Ordinary program synthesis.

NOT LEVEL 1 (improved search efficiency).
NOT LEVEL 2 (reusable structural abstraction).
NOT LEVEL 3 (cross-family transfer).
NOT LEVEL 4 (open-ended discovery).

## RELEASE VERDICT: NO

The v28 signal was not robust.
It disappears under stronger controls.
The claim should not be expanded.

## SCIENTIFIC VERDICT

Null hypothesis:
  H0: ACID has no meaningful advantage over ordinary search.

Observed effect:
  v28: ACID 3/24, BF 0/24 (non-robust)
  v29: B0 0/12, B2 0/12 (no advantage)

Replication:
  The v28 signal does NOT replicate with different task instances.
  The advantage disappears under stronger controls.

Effect size: ZERO (under replication)

Evidence for reusable abstraction: NO
Evidence for general capability: NO

CONCLUSION D: The 3/24 signal disappears under stronger controls.

The v28 result was likely due to stochastic variance
and benchmark-specific alignment, not a real capability.

RELEASE VERDICT: NO

The signal was not robust.
The claim should not be expanded.
