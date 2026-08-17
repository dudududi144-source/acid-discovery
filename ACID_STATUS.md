# ACID STATUS

## System: OPERATIONAL (with limitations)

## Version: 10.0.0

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## Package: 27 modules (125KB)

## Substrate: 20 primitives
PUSH, POP, DUP, SWAP, ADD, SUB, MUL, MOD,
GT, LT, EQ, AND, OR, NOT, JZ, READ, WRITE, STORE, LOAD, HALT

## ARITHMETIC DOMAIN
- Modular arithmetic (mod 1,000,000): PROVEN
- Integer arithmetic: FAILED (negative sums wrap)
- CLAIM = MODULAR ARITHMETIC ONLY

## AUDIT FINDINGS (2026-08-16)

### PROVEN
- Positive-domain solving: 10/10 tasks, 10000/10000 each
- Modular arithmetic: 10000/10000 with negative inputs
- Blind generalization: 10/10 tasks, 100000/100000
- Reproducibility: 3/3 identical
- Constant rejection: 93/93 rejected

### NOT PROVEN
- Transfer (artifact = answer, this is retrieval)
- Self-improvement (not monotonic)
- Mutation contribution (0% = 50%)
- Verification contribution (not needed for discovery)
- Seed reliability (41/100 without artifact)

### COUNTEREXAMPLES FOUND
1. Modulo assumption (negative sums wrap)
2. Seed sensitivity (1/10 without artifact)
3. Artifact = answer (retrieval, not transfer)

## CAUSAL MECHANISM

The artifact IS the causal mechanism.
The search provides 9pp improvement over random.
Mutation, verification, transfer are not causal.

## Last Updated
2026-08-16
