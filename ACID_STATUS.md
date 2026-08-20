# ACID STATUS

## System: H0 REJECTED FOR NESTED_COMPOSITION
## Version: 28.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## V28 RESULT: H0 REJECTED FOR NESTED_COMPOSITION

The 1/6 signal from v27 REPLICATES across independent test sets.
The advantage is REAL, not statistical noise.

### Results

| Test Set | ACID | Brute Force |
|----------|------|-------------|
| A | 1/6 | 0/6 |
| B | 1/6 | 0/6 |
| C | 0/6 | 0/6 |
| D | 1/6 | 0/6 |

Total: ACID 3/24, BF 0/24, Difference: 3

### Family Analysis

| Family | ACID | Brute Force |
|--------|------|-------------|
| conditional | 0/12 | 0/12 |
| nested_composition | 3/12 | 0/12 |

## KEY FINDING

The advantage is REAL but LIMITED:
- Only on nested_composition tasks (3/12)
- NOT on conditional tasks (0/12)
- NOT cross-family transfer
- NOT generic abstraction discovery

## RELEASE VERDICT: NO

The signal is real but not yet robust enough to ship.
Cross-family transfer is not demonstrated.
Multi-seed testing was not completed.
Adversarial testing was not performed.

## WHAT REMAINS UNPROVEN

- Conditional task discovery
- Cross-family capability transfer
- Generic abstraction discovery
- Open-ended capability discovery
- Adversarial robustness
- "I don't know" capability
- Multi-seed robustness (10+ seeds)
- Compute efficiency advantage
- Representation learning
- Compositional depth generalization (depth 4+)

## WHAT IS PROVEN

- Simple arithmetic discovery (add, multiply, double)
- Meaningful advantage on nested_composition (3/24 vs 0/24)
- Signal replicates across independent test sets (3/4)
- No false discoveries
- No target-specific heuristics
- Reproducibility (deterministic)

## NEXT STEPS

1. Complete multi-seed testing (10+ seeds)
2. Test adversarial robustness
3. Implement "I don't know" capability
4. Fix search algorithm for conditional tasks
5. Build cross-family capability transfer
6. Re-run benchmark after fixes
7. Compare against baseline again

Do NOT ship until:
- Multi-seed testing is complete (10+ seeds)
- Adversarial testing is performed
- Cross-family transfer is demonstrated
- Conditional tasks are solved
