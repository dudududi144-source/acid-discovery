# ACID - Autonomous Computational Intelligence Discovery

## IMPORTANT: AUDIT FINDINGS

This system has been subjected to a blind adversarial scientific audit.
The findings are documented in AUDIT_RESULTS.md.

### What is PROVEN:
- Positive-domain program synthesis (10/10 tasks, 10000/10000 held-out)
- Modular arithmetic (mod 1,000,000) with negative inputs
- Blind generalization on unseen tasks (10/10 tasks, 100000/100000)
- Reproducibility (3/3 identical runs)
- Constant/overfit program rejection (93/93 rejected)

### What is NOT PROVEN:
- Transfer (the artifact was the answer, this was retrieval)
- Self-improvement (not monotonic)
- Mutation contribution (0% = 50% with artifact)
- Verification contribution (not needed for discovery)
- Seed reliability (41/100 without artifact)

### COUNTEREXAMPLES FOUND:
1. Modulo assumption: negative sums wrap around
2. Seed sensitivity: only 41/100 seeds succeed without artifact
3. Artifact = answer: the "transfer" was actually retrieval

### CAUSAL MECHANISM:
The artifact IS the causal mechanism.
The search provides 9pp improvement over random.
Mutation, verification, transfer are not causal.

## ARITHMETIC DOMAIN

CLAIM = MODULAR ARITHMETIC ONLY

The substrate uses (a + b) % 1000000.
Negative results wrap around.
This system does NOT perform integer arithmetic.

## Substrate: 20 Primitives

PUSH, POP, DUP, SWAP, ADD, SUB, MUL, MOD,
GT, LT, EQ, AND, OR, NOT, JZ, READ, WRITE, STORE, LOAD, HALT

## Deployed

- UI + API: https://acid-api.rabotatony.workers.dev
- Repo: https://github.com/dudududi144-source/acid-discovery

## Audit Trail

See AUDIT_RESULTS.md for complete findings.
See ACID_STATUS.md for current status.
