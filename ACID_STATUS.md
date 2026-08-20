# ACID STATUS

## System: RELEASE VERDICT = NO
## Version: 26.0.0 (brutal red-team)
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## RELEASE VERDICT: NO

ACID does not outperform brute force under matched compute.
The capability is not yet real. Shipping would be premature.

## LEADERBOARD

| Version | Benchmark | Success | False Discoveries | Reproducibility |
|---------|-----------|---------|-------------------|-----------------|
| v26.0.0 | 12 tasks | 5/12 | 0 | YES |

### Results by Category

| Category | Pass | Fail | Total |
|----------|------|------|-------|
| A_easy_wins | 3 | 0 | 3 |
| B_known_hard | 0 | 3 | 3 |
| C_adversarial | 1 | 2 | 3 |
| D_anti_acid | 1 | 2 | 3 |
| TOTAL | 5 | 7 | 12 |

## BASELINE COMPARISON

Brute force (5000 candidates) solves 5/12 tasks.
ACID adds NO value beyond brute force under matched compute.
BASELINE BEATS ACID on conditional and composition tasks.

## IRON LAW APPLIED

When choosing between:
A. Making the product look more impressive
B. Revealing that the product is less good than we thought

We chose B.

True negative information is worth more than ten fake successes.

## WHAT REMAINS UNPROVEN

- Generic abstraction discovery
- Cross-family capability transfer
- Self-directed frontier expansion
- Open-ended capability discovery
- Conditional task discovery (max, min)
- Composition task discovery
- Adversarial robustness
- "I don't know" capability

## SHOULD WE SHIP? NO

The capability is not yet real.
Shipping would be premature.

## NEXT STEPS

1. Fix the search algorithm to handle conditional tasks
2. Implement generic structural abstraction discovery
3. Build cross-family capability transfer
4. Implement "I don't know" capability
5. Build adversarial robustness
6. Re-run benchmark after fixes
7. Compare against baseline again

Do NOT ship until the benchmark shows ACID outperforming
brute force under matched compute on conditional and
composition tasks.
