# ACID STATUS

## System: CONCLUSION D - SIGNAL DISAPPEARS UNDER STRONGER CONTROLS
## Version: 29.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## V29 RESULT: CONCLUSION D

The v28 signal (3/24) does NOT replicate with different task instances.
The advantage disappears under stronger controls.

### Results

| System | Solved | Mean Fit |
|--------|--------|----------|
| B0 (Brute force) | 0/12 | 0.044-0.067 |
| B2 (Evolutionary) | 0/12 | 0.0-0.044 |

Difference: 0

### Mechanism Analysis

The v28 result was NOT robust.
It depended on specific task instances that happened to be
easier for evolutionary search.

When the task instances change, the advantage disappears.

## CONCLUSION D: THE 3/24 SIGNAL DISAPPEARS UNDER STRONGER CONTROLS

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

## WHAT REMAINS UNPROVEN

- Generic abstraction discovery
- Cross-family capability transfer
- Self-directed frontier expansion
- Open-ended capability discovery
- Conditional task discovery
- Composition task discovery
- Adversarial robustness
- "I don't know" capability
- Multi-seed robustness
- Compute efficiency advantage
- Representation learning
- Compositional depth generalization

## WHAT IS PROVEN

- Simple arithmetic discovery (add, multiply, double)
- No false discoveries
- No target-specific heuristics
- Reproducibility (deterministic)

## COMPLETE PROJECT HISTORY (v22-v29)

v22: Conditional composition PROVEN (but hardcoded max detection)
v23: Recursive frontier expansion PROVEN (but researcher curriculum)
v24: Adversarial audit found methodological problems
v25: Matched compute: 4/10 solved
v26: Brutal red-team: 5/12 solved, RELEASE VERDICT: NO
v27: Generalization: 1/6 weak signal
v28: Prove the signal: 3/24 replicates (non-robust)
v29: Explain the advantage: CONCLUSION D - signal disappears

## FINAL VERDICT

The ACID project has demonstrated:
  - Ordinary program synthesis with evolutionary search
  - Simple arithmetic discovery
  - No false discoveries
  - No target-specific heuristics

The ACID project has NOT demonstrated:
  - Generic abstraction discovery
  - Cross-family capability transfer
  - Self-directed frontier expansion
  - Open-ended capability discovery
  - Meaningful advantage over ordinary search

The v28 signal was not robust.
It disappears under stronger controls.

ACID is ordinary program synthesis with evolutionary search.
It does NOT demonstrate capability discovery or frontier expansion.
