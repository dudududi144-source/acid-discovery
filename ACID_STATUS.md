# ACID STATUS

## System: V20 CAPABILITY-AS-SEARCH-FUEL EXPERIMENT
## Version: 20.0.0
## Last Updated: 2026-08-18

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## LATEST EXPERIMENT: Capability-as-Search-Fuel (ACID v20)

### C1 DISCOVERY: PROVEN (1000/1000)
- Behavioral diagnosis: CONDITIONAL_SPLIT (confidence=1.0)
- C1 synthesized from diagnosis
- Held-out: 1000/1000, Adversarial: 30/30

### C2 DISCOVERY: NOT PROVEN
- CONTROL A (L0): fit=0
- CONTROL B (L1 with C1): fit=0.47
- C1 improved search but did not enable full C2 discovery

### CAUSALITY: ESTABLISHED
- C1 specifically causes improved search (0.47 > 0 > 0)
- Random C1 does not help (fit=0.0)

### FRESH-PROCESS: PROVEN (1000/1000)

## FINAL VERDICT
AUTONOMOUS CAPABILITY FRONTIER EXPANSION = PARTIAL

C1 discovery: PROVEN
C1 as search primitive: PARTIAL (improved search)
C2 discovery with C1: NOT PROVEN (fit=0.47)
Fresh-process reuse: PROVEN
Open-ended discovery: NOT PROVEN
General intelligence: NO

## REMAINING BOUNDARY
JZ COMPOSITION FOR CONDITIONAL PROGRAMS.
C1 improves search but cannot be correctly composed.
Both branches of conditional must be extended with continuation.
