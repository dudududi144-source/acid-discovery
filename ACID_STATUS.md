# ACID STATUS

## System: EVOLUTIONARY DISCOVERY EXPERIMENT COMPLETE
## Version: 15.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## LATEST EXPERIMENT: Evolutionary Search Discovery

### Key Result: EVOLUTIONARY > RANDOM SEARCH
- Random search: 2/6 discovered
- Evolutionary search: 3/6 discovered
- Improvement: multiplication (T2) discovered

### Discovered Constructs (3/6)
- T1 subtraction: 1000/1000, CASE_4_SUBSTRATE_DERIVED
- T2 multiplication: 1000/1000, CASE_4_SUBSTRATE_DERIVED
- T5 modulo: 1000/1000, CASE_4_SUBSTRATE_DERIVED

### Not Discovered (3/6)
- T3 max: fit=0.75, CASE_3_REQUIRES_COMPOSITION
- T4 abs_diff: fit=0.75, CASE_3_REQUIRES_COMPOSITION
- T6 exponentiation: CORRECTLY REJECTED (impossible)

### Verification
- Falsification: 30/30 (all discovered constructs)
- Held-out: 1000/1000 (all discovered constructs)
- Fresh-process reuse: 100/100 (all capabilities)
- Blind transfer: 1000/1000
- Composition: 1000/1000
- Frontier expansion: FAILED (0/100)
- Negative control: PROVEN (impossible rejected)

### Boundary Shift
Previous boundary: THE SUBSTRATE
Current boundary: SEARCH DEPTH FOR COMPOSITION

The substrate CAN express max, abs, compositions.
The search CANNOT find them in 100 generations.
The boundary is the SEARCH ALGORITHM's depth.

## Complete Experiment History
1. Substrate + Search: PROVEN
2. Construct Discovery: PROVEN
3. Falsification: PROVEN
4. Composition (depth 3): PROVEN
5. Repair: PROVEN
6. Blind Adversarial Replication: PARTIAL
7. Full-Substrate Boundary Closure: PROVEN
8. Open-Ended Discovery (random): PARTIAL (2/6)
9. Open-Ended Discovery (evolutionary): PARTIAL (3/6)

## Final Verdict
SUBSTRATE-DERIVED CONSTRUCT DISCOVERY = PROVEN (3/6)
EVOLUTIONARY > RANDOM SEARCH = PROVEN (3/6 vs 2/6)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
CAPABILITY LANGUAGE EXTENSION = PARTIAL
FRONTIER EXPANSION = FAILED
GENERAL INTELLIGENCE = NO

## Next Highest-Information Experiment
Capability-guided search: use discovered constructs
(sub, mul) as building blocks and search for
compositions using them. This should enable
CASE_3 discovery (max, abs, conditional).
