# ACID STATUS

## System: CONDITIONAL DISCOVERY FIX COMPLETE
## Version: 17.1.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## LATEST EXPERIMENT: Conditional Discovery Fix (ACID v17.1)

### Known Max Solution: FIXED AND VERIFIED
- Previous max_prog had a bug (JZ target wrong)
- Fixed max_prog: 1000/1000 held-out, 30/30 adversarial
- Substrate CAN express conditional operations

### Search Results
- Evolutionary search: fit=0.6 after 50000 candidates
- Search CANNOT find conditional branching patterns
- Boundary: SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS

### Composition Results
- max(x0,x1)+x2: 490/1000 (partial)
- Bug: JZ targets are absolute indices, break on extension
- Composition of jump programs requires jump target adjustment

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
12. Conditional Discovery Fix: KNOWN SOLUTION VERIFIED, SEARCH FAILED

## Final Verdict
SUBSTRATE-DERIVED CONSTRUCT DISCOVERY = PROVEN (3/6)
EVOLUTIONARY > RANDOM SEARCH = PROVEN (3/6 vs 2/6)
SUBSTRATE EXPRESSIVITY (CONDITIONAL) = PROVEN (1000/1000)
SEARCH DISCOVERY OF CONDITIONAL PATTERNS = NOT PROVEN (fit=0.6)
COMPOSITION OF JUMP PROGRAMS = PARTIAL (490/1000)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
GENERAL INTELLIGENCE = NO

## Remaining Bottleneck
SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.
The substrate CAN express conditional operations.
The search CANNOT find them.
Composition of jump programs requires jump target adjustment.
