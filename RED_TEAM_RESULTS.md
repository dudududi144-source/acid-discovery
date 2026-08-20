# ACID v26: Brutal Red-Team Build Results

## Date: 2026-08-18

## RELEASE VERDICT: NO

ACID does not outperform brute force under matched compute.
The capability is not yet real. Shipping would be premature.

## LEADERBOARD

| Version | Benchmark | Success | False Discoveries | Time | Compute | Reproducibility |
|---------|-----------|---------|-------------------|------|---------|-----------------|
| v26.0.0 | 12 tasks | 5/12 | 0 | deterministic | 5000 candidates | YES |

### Results by Category

| Category | Pass | Fail | Total |
|----------|------|------|-------|
| A_easy_wins | 3 | 0 | 3 |
| B_known_hard | 0 | 3 | 3 |
| C_adversarial | 1 | 2 | 3 |
| D_anti_acid | 1 | 2 | 3 |
| TOTAL | 5 | 7 | 12 |

### Individual Results

| Task | Category | Fit | Eval Accuracy | Status |
|------|----------|-----|---------------|--------|
| identity | A_easy_wins | 1.0 | 1.0 | PASS |
| add2 | A_easy_wins | 1.0 | 1.0 | PASS |
| double | A_easy_wins | 1.0 | 1.0 | PASS |
| add3 | B_known_hard | 0.13 | 0.0 | FAIL |
| add4 | B_known_hard | 0.07 | 0.0 | FAIL |
| max2 | B_known_hard | 0.73 | 0.0 | FAIL |
| false_pattern | C_adversarial | 1.0 | 1.0 | PASS |
| overfit_trap | C_adversarial | 0.8 | 0.96 | FAIL |
| no_solution | C_adversarial | 0.13 | 0.0 | FAIL |
| brute_force_wins | D_anti_acid | 1.0 | 1.0 | PASS |
| conditional_branch | D_anti_acid | 0.87 | 0.4 | FAIL |
| i_dont_know | D_anti_acid | 0.33 | 0.0 | FAIL |

## FAILURE TAXONOMY

| Task | Failure Type | Fit |
|------|-------------|-----|
| add3 | SEARCH_EXPLOSION | 0.13 |
| add4 | UNSOLVED | 0.07 |
| max2 | OVERFIT | 0.73 |
| overfit_trap | OVERFIT | 0.8 |
| no_solution | SEARCH_EXPLOSION | 0.13 |
| conditional_branch | OVERFIT | 0.87 |
| i_dont_know | SEARCH_EXPLOSION | 0.33 |

## BASELINE COMPARISON

Brute force (5000 candidates) solves 5/12 tasks.
ACID adds NO value beyond brute force under matched compute.

BASELINE BEATS ACID on conditional and composition tasks.
This is a RESULT, not a bug in the report.

## CLAIMS STATUS

| Claim | Status |
|-------|--------|
| ACID can discover programs matching behavioral examples | PROVEN (easy tasks only) |
| ACID discovers programs faster than brute force | NOT PROVEN |
| ACID discovers programs not findable by baseline | NOT PROVEN |
| Discovered capabilities generalize to unseen tasks | NOT PROVEN |
| Autonomous capability frontier expansion | UNVERIFIED |
| Generic abstraction discovery | UNVERIFIED |
| Cross-family capability transfer | UNVERIFIED |
| Recursive capability expansion | UNVERIFIED |

## RELEASE VERDICT

What we claim:
  ACID can discover programs matching behavioral examples
  via evolutionary search over a 20-primitive substrate.

What we actually demonstrated:
  - Easy wins (identity, add2, double): SOLVED
  - Known hard (add3, add4, max2): NOT SOLVED under matched compute
  - Adversarial (false_pattern, overfit_trap, no_solution): NOT SOLVED
  - Anti-ACID (brute_force_wins, conditional_branch, i_dont_know): NOT SOLVED

Best result:
  5/12 tasks solved under matched compute (5000 candidates)

Worst result:
  Conditional tasks (max, min): fit=0.67, NEVER solved across 10 seeds
  Composition tasks: fit=0.07-0.6, NOT solved
  Adversarial tasks: NOT solved

Baseline comparison:
  Brute force (5000 candidates) solves 5/12 tasks.
  ACID adds NO value beyond brute force under matched compute.
  BASELINE BEATS ACID on conditional and composition tasks.

False discovery rate:
  0 false discoveries (no incorrect programs claimed as discoveries)

Reproducibility:
  Deterministic (fixed seeds). Reproducible.

Known failures:
  - Conditional tasks: NOT SOLVED (fit=0.67)
  - Composition tasks: NOT SOLVED (fit=0.07-0.6)
  - Adversarial tasks: NOT SOLVED
  - Anti-ACID tasks: NOT SOLVED

Unverified claims:
  - "Autonomous capability frontier expansion" -> UNVERIFIED
  - "Generic abstraction discovery" -> UNVERIFIED
  - "Cross-family capability transfer" -> UNVERIFIED
  - "Recursive capability expansion" -> UNVERIFIED

What would falsify our hypothesis:
  If brute force with 2x budget solves all tasks that
  ACID claims to solve via "capability expansion",
  then ACID adds no value.

Should we ship? NO

Reason:
  ACID does not outperform brute force under matched compute.
  The "frontier expansion" claim from v23/v24 was invalidated
  by the v25 adversarial audit (hardcoded max detection,
  researcher-designed curriculum, unequal compute).
  
  The current system is ordinary program synthesis with
  evolutionary search. It does not demonstrate:
  - Generic abstraction discovery
  - Cross-family capability transfer
  - Self-directed frontier expansion
  - Open-ended capability discovery
  
  Shipping would be premature.
  The capability is not yet real.

## IRON LAW APPLIED

When choosing between:
A. Making the product look more impressive
B. Revealing that the product is less good than we thought

We chose B.

True negative information is worth more than ten fake successes.
