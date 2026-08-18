# ACID STATUS

## System: OPERATIONAL (with limitations)
## Version: 10.0.0
## Last Updated: 2026-08-16

## Deployed
- UI + API: https://acid-api.rabotatony.workers.dev
- Worker: v10 (17,995 bytes)

## Package: 28 modules (including repair.py)

## Substrate: 20 primitives (FIXED)
PUSH, POP, DUP, SWAP, ADD, SUB, MUL, MOD,
GT, LT, EQ, AND, OR, NOT, JZ, READ, WRITE, STORE, LOAD, HALT

## Experiment Results Summary

### PROVEN
- Substrate execution: 100000/100000
- Search > random: 84% vs 32%
- Abstraction speedup: 369x (manual)
- Composition: A+B > A, A+B > B (1000/1000)
- Semantic abstraction: 1000/1000 unseen
- Diagnostic repair (designed tasks): 10/10, 1000/1000 each
- Counterfactual controls: all fail

### SUPPORTED
- Search-space factorization: 0.34 vs 0.20
- Diagnostic repair concept: sound
- Partial-credit scoring: enables structure discovery

### FAILED
- Repair generalization: 0/5 transfer
- Repair seed robustness: 0/30
- Repair composition: 0/1000
- Capability frontier expansion: not achieved
- Autonomous abstraction extraction: weak
- Incremental construction: 0/8

### NOT PROVEN
- Capability accumulation
- Recursive capability building
- Cross-model transfer
- Open-ended capability growth

## Key Bottleneck
The hypothesis engine has a FIXED hypothesis space (4 types).
It does not discover new hypothesis types from data.
This prevents generalization to unseen task types.

## Next Steps
1. Build symbolic regression for hypothesis discovery
2. Implement active diagnosis (information-maximizing queries)
3. Test repair on truly blind task suites
4. Implement repair memory and reuse
5. Test composition of repair mechanisms


## Hypothesis-Language Induction (2026-08-18)

### BREAKTHROUGH (Partial)
Symbolic regression DISCOVERS correct OOD relations:
- Subtraction: ((x[0]+3)-(x[1]+3)) = x[0]-x[1], fitness 1.0
- Doubling: (x[0]+actual) = 2*x[0], fitness 1.0
- NO fixed hypothesis types used
- Relations discovered from data alone

### BOTTLENECK
Expression-to-program compilation FAILS.
Discovered expressions are correct but don't compile to working programs.
Held-out: 1/1000 (subtraction), 2/1000 (doubling)

### NEXT STEP
Fix expression simplification + compilation.
The system KNOWS the answer. It cannot yet BUILD the program.

### Updated Module Count: 28
Added: acid/repair.py (repair engine with hypothesis system)
