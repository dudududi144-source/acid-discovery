# ACID Blind Adversarial Replication Results

## Date: 2026-08-18

## BLIND CLASSIFICATION: 6/12 (initial), 7/8 (boundary closure)

### Key Findings

1. DIRECT REUSE: PROVEN (7/12 tasks solved by existing capabilities)
2. ARGUMENT-SHIFT DETECTION: FAILED initially, PROVEN in boundary closure
3. ADVERSARIAL ROBUSTNESS: PROVEN (mod-999 trap caught)
4. NEAR-MATCH REJECTION: PROVEN (3/3 correct)
5. OUT-OF-LANGUAGE REJECTION: PROVEN (3/3 correct)
6. REPAIR-OF-REPAIR: NOT TRIGGERED (existing caps found)
7. NEW CAPABILITY DISCOVERY: NOT PROVEN (term space fixed)

### Multi-Seed Results

- Composition: 30/30 seeds pass
- Repair: 10/10 seeds pass (within scope)
- Blind repair: 0/10 (substrate limitation)

### Controls

All controls fail correctly:
- Random capability: 0/100
- Wrong capability: 0/100
- Wrong order: 0/100
- Original (unrepaired): 0/100 on repair tasks

### Capability Library (Final)

| Capability | Semantic | Version | Status |
|-----------|----------|---------|--------|
| cap_A | square(x0) | v1 | VERIFIED |
| cap_B | add(x0,x1) | v1 | VERIFIED |
| cap_C | square(x0)+x1 | v1 | VERIFIED |
| cap_C_v2 | square(x0)+x1+x2 | v2 | REPAIRED |
| cap_E | square(x0)+x1+square(x2) | v1 | VERIFIED |
| cap_G | square(x0)+x1+square(x2)+x3 | v1 | VERIFIED |
| cap_D | (square(x0)+x1+x2)+square(x3) | v1 | VERIFIED |

### Dependency Graph

cap_A + cap_B -> cap_C
cap_C + cap_A -> cap_E
cap_E + cap_B -> cap_G
cap_C.v1 -> cap_C.v2 (repair lineage)
cap_C_v2 + cap_A -> cap_D

### Final Verdict

OPEN-ENDED CAPABILITY ACCUMULATION = PARTIAL

The capability lifecycle is demonstrated within the
representational scope of the fixed substrate.

The boundary is the substrate itself:
- Cannot reorder inputs (no SWAP/STORE/LOAD)
- Cannot discover new operations
- Cannot extend the term space

CAPABILITY REPAIR = PROVEN (within scope)
BLIND ADVERSARIAL ROBUSTNESS = PARTIAL
GENERAL INTELLIGENCE = NO
