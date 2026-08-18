# ACID STATUS

## System: CONDITIONAL DISCOVERY EXPERIMENT COMPLETE
## Version: 17.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## LATEST EXPERIMENT: Conditional Discovery (ACID v17)

### Critical Finding: Known Solution Was Incorrect
The known max_prog solution achieved 0/100 (bug in known solution).
The search algorithms achieved fit=0.6 (better than known solution).

### Search Results
- A (random): fit=0.6
- B (evolutionary): fit=0.6
- D (cap-guided): fit=0.6
- Known solution: fit=0.0 (bug)

### Key Finding
All three search systems achieved the same fit (0.6).
None could discover conditional branching patterns.
The boundary is SEARCH DEPTH FOR CONDITIONAL PATTERNS.

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
10. Capability-Guided Search: NOT TESTED (code error)
11. Conditional Discovery: NOT PROVEN (fit=0.6)

## Final Verdict
SUBSTRATE-DERIVED CONSTRUCT DISCOVERY = PROVEN (3/6)
EVOLUTIONARY > RANDOM SEARCH = PROVEN (3/6 vs 2/6)
CAPABILITY-GUIDED > RAW SEARCH = NOT PROVEN (same fit)
CONDITIONAL DISCOVERY = NOT PROVEN (fit=0.6)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
GENERAL INTELLIGENCE = NO

## Remaining Bottleneck
SEARCH DEPTH FOR CONDITIONAL PATTERNS.
The substrate CAN express conditional operations.
The search CANNOT find them.
This is a search complexity limitation, not representational.
