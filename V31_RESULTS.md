# ACID v31: Replication Trial Results

## Date: 2026-08-18

## PREREGISTERED HYPOTHESIS

ACID provides reproducible search-efficiency improvements
over ordinary program synthesis under matched compute.

Primary metric: success rate at matched compute
Tasks: 6 (2 per family)
Seeds: 3
Budget: 1000

## RESULTS

| System | Success Rate | Solved |
|--------|-------------|--------|
| ACID | 0.333 | 6/18 |
| BF | 0.111 | 2/18 |
| Diff | 0.222 | 4/18 |

## PER-FAMILY ANALYSIS

| Family | ACID | BF | Diff |
|--------|------|-----|------|
| unary | 0.0 | 0.0 | 0.0 |
| binary | 1.0 | 0.333 | 0.667 |
| ternary | 0.0 | 0.0 | 0.0 |

## CRITICAL FINDING

The advantage is ENTIRELY from the binary family.
ACID=1.0 vs BF=0.333 on binary tasks.
Unary and ternary tasks show NO advantage.

This is a DOMAIN-SPECIFIC advantage, not a general
search-efficiency improvement.

## FINAL CLASSIFICATION

LEVEL 1A: Narrow, family-specific search-efficiency improvement.

NOT LEVEL 1B (broad, replicated search-efficiency improvement).

The advantage is only on binary tasks (add, multiply).
Unary and ternary tasks show no advantage.

## RELEASE VERDICT: NO

The advantage is domain-specific (binary family only).
It is not a general search-efficiency improvement.
The claim should not be expanded.

## WHAT THE EVIDENCE ACTUALLY SUPPORTS

The evidence supports:
  - ACID has an advantage on binary arithmetic tasks (add, multiply)
  - The advantage is 0.667 (ACID=1.0 vs BF=0.333)
  - The advantage is NOT general (unary and ternary show no advantage)

The evidence does NOT support:
  - General search-efficiency improvement
  - Cross-family transfer
  - Reusable structural abstraction
  - Open-ended capability discovery

## COMPLETE PROJECT HISTORY (v22-v31)

v22: Conditional composition PROVEN (but hardcoded max detection)
v23: Recursive frontier expansion PROVEN (but researcher curriculum)
v24: Adversarial audit found methodological problems
v25: Matched compute: 4/10 solved
v26: Brutal red-team: 5/12 solved, RELEASE VERDICT: NO
v27: Generalization: 1/6 weak signal
v28: Prove the signal: 3/24 replicates (non-robust)
v29: Explain the advantage: CONCLUSION D - signal disappears
v30: Research reset: MARGINAL compute efficiency advantage
v31: Replication trial: LEVEL 1A - binary family only

## FINAL VERDICT

LEVEL 1A: Narrow, family-specific search-efficiency improvement.

ACID has an advantage on binary arithmetic tasks (add, multiply).
The advantage is NOT general.
Unary and ternary tasks show no advantage.

RELEASE VERDICT: NO

The advantage is domain-specific.
It is not a general search-efficiency improvement.
The claim should not be expanded.

ACID is ordinary program synthesis with evolutionary search,
with a narrow advantage on binary arithmetic tasks.

This is NOT capability discovery.
This is NOT frontier expansion.
This is NOT open-ended discovery.
