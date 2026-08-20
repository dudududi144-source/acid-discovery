# ACID STATUS

## System: LEVEL 1A - BINARY FAMILY ONLY
## Version: 31.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## V31 RESULT: LEVEL 1A - BINARY FAMILY ONLY

ACID has an advantage on binary arithmetic tasks (add, multiply).
The advantage is NOT general.
Unary and ternary tasks show no advantage.

### Results

| System | Success Rate | Solved |
|--------|-------------|--------|
| ACID | 0.333 | 6/18 |
| BF | 0.111 | 2/18 |
| Diff | 0.222 | 4/18 |

### Per-Family Analysis

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

## LEVEL

LEVEL 1A: Narrow, family-specific search-efficiency improvement.

NOT LEVEL 1B (broad, replicated search-efficiency improvement).
NOT LEVEL 2 (reusable structural abstraction).
NOT LEVEL 3 (cross-family transfer).
NOT LEVEL 4 (open-ended discovery).

## RELEASE VERDICT: NO

The advantage is domain-specific (binary family only).
It is not a general search-efficiency improvement.
The claim should not be expanded.

## WHAT REMAINS UNPROVEN

- General search-efficiency improvement
- Cross-family capability transfer
- Self-directed frontier expansion
- Open-ended capability discovery
- Conditional task discovery
- Composition task discovery
- Adversarial robustness
- "I don't know" capability
- Multi-seed robustness (20+ seeds)
- Representation learning
- Compositional depth generalization

## WHAT IS PROVEN

- Simple arithmetic discovery (add, multiply, double)
- Narrow advantage on binary arithmetic tasks (add, multiply)
- No false discoveries
- No target-specific heuristics
- Reproducibility (deterministic)

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
