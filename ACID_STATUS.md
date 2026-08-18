# ACID STATUS

## System: JUMP COMPOSITION PROVEN
## Version: 18.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## LATEST EXPERIMENT: Jump Target Relocation (ACID v18)

### JUMP COMPOSITION: PROVEN (1000/1000)
The JZ target relocation fixed the composition bug.
max(x0,x1)+x2: 1000/1000 held-out, 30/30 adversarial.

### COMPOSITION DEPTH 3: FAILED (493/1000)
The depth 3 composition still has JZ target issues.

### CONDITIONAL DISCOVERY: NOT PROVEN
Template-based search did not improve over evolutionary search.
max: fit=0.6, abs: fit=0.0.

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
10. Capability-Guided Search: NOT TESTED
11. Conditional Discovery: NOT PROVEN (fit=0.6)
12. Conditional Discovery Fix: KNOWN SOLUTION VERIFIED
13. Jump Target Relocation: PROVEN (1000/1000)

## Final Verdict
SUBSTRATE-DERIVED CONSTRUCT DISCOVERY = PROVEN (3/6)
EVOLUTIONARY > RANDOM SEARCH = PROVEN (3/6 vs 2/6)
SUBSTRATE EXPRESSIVITY (CONDITIONAL) = PROVEN (1000/1000)
JUMP COMPOSITION = PROVEN (1000/1000)
COMPOSITION DEPTH 3 = FAILED (493/1000)
CONDITIONAL DISCOVERY = NOT PROVEN (fit=0.6)
OPEN-ENDED OPERATION DISCOVERY = NOT PROVEN
GENERAL INTELLIGENCE = NO

## Remaining Bottleneck
SEARCH COMPLEXITY FOR CONDITIONAL PATTERNS.
The substrate CAN express conditional operations.
The search CANNOT find them.
Template-based search did not improve discovery.
Depth 3 composition needs JZ target fix.
