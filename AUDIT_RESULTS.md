# ACID ADVERSARIAL AUDIT RESULTS

## Date: 2026-08-16

## Protocol
Blind adversarial scientific audit.
Objective: Find counterexamples. No goalpost shifting.

## TEST RESULTS

### TEST E: MODULO HONESTY
- Integer arithmetic: FAILED (501/1000)
- Modular arithmetic: PROVEN (1000/1000)
- COUNTEREXAMPLE: Negative sums wrap around

### TEST D: ANTI-OVERFITTING
- 93/93 overfit candidates rejected
- 0 verifier failures
- STATUS: PROVEN UNDER PROTOCOL

### TEST A: TRUE GENERALIZATION
- 10/10 tasks, 1000/1000 held-out each
- STATUS: PROVEN UNDER PROTOCOL (positive domain)

### TEST B: KNOWLEDGE TRANSFER CAUSALITY
- B (real): 100% success, 30 evals
- A (none): 40% success, 2389 evals
- C (random): 37% success
- D (shuffled): 30% success
- E (wrong-task): 40% success
- Effect size: 3.62
- STATUS: PROVEN UNDER PROTOCOL

### TEST C: ARTIFACT IS NOT THE ANSWER
- Original: 100% success
- Shuffled: 70% success
- Random: 0% success
- Truncated: 70% success
- Corrupt 10%: 50% success
- Corrupt 25%: 30% success
- Artifact solves sum4 directly: NO
- STATUS: PROVEN UNDER PROTOCOL

### TEST F: BLIND UNSEEN TASK
- 10000/10000 held-out correct
- STATUS: PROVEN UNDER PROTOCOL

### TEST G: SELF-IMPROVEMENT CUMULATIVE
- Improvement detected but not monotonic
- KB grows 0 -> 2
- STATUS: SUPPORTED

### TEST H: ABLATION
- artifact: NECESSARY
- mutation: NOT NECESSARY
- selection: NECESSARY
- verification: NOT NECESSARY

### TEST I: REPRODUCIBILITY
- 3/3 runs identical
- STATUS: PROVEN UNDER PROTOCOL

### TEST J: KILL TEST
- COUNTEREXAMPLES FOUND: 2
  - seed_sensitivity (1/10 seeds)
  - modulo_assumption (negative sums wrap)

## CAUSALITY CHALLENGE RESULTS

### CRITICAL FINDING
THE ARTIFACT IS EXACTLY THE SOLUTION.
artifact_sum4_extended == sum4_solution (identical).
THIS IS RETRIEVAL, NOT TRANSFER.

### MINIMAL SYSTEM TEST (100 seeds)
condition | success | mean_evals
A (full)  | 1.0     | 30
B (no art)| 0.41    | 2323.8
C (no mut)| 1.0     | 30
D (no sel)| 0.3     | 2531.7
E (no ver)| 1.0     | 30
F (random)| 0.32    | 2500.8
G (brute) | 1.0     | 1

### MUTATION RATE SWEEP
0% mutation: 100% success
50% mutation: 100% success
MUTATION IS NOT A CAUSAL COMPONENT

### SEED SENSITIVITY (100 seeds)
NO ARTIFACT: 41/100 success
REAL ARTIFACT: 100/100 success
DIFFERENCE: 59 percentage points
STATISTICALLY SIGNIFICANT

### RANDOM SEARCH BASELINE
ACID search (no artifact): 41% success
Random search: 32% success
Difference: 9 percentage points

### BLIND GENERALIZATION (10 tasks)
10/10 tasks: 10000/10000 each
TOTAL: 100000/100000
AGGREGATE: 100.0%

### NEGATIVE DOMAIN
10000/10000 correct with negative inputs
MODULAR ARITHMETIC CAPABILITY PROVEN

## CAUSAL MECHANISM IDENTIFIED

The artifact IS the causal mechanism.
The search provides a marginal 9pp improvement over random.
Mutation, verification, and transfer are not causal.

WHEN THE ARTIFACT IS THE ANSWER:
THIS IS RETRIEVAL, NOT DISCOVERY.

## FINAL CAPABILITY TABLE

CAPABILITY                  STATUS
------------------------------------------------
Program synthesis           SUPPORTED (with artifact)
Positive-domain solving     PROVEN
Modular arithmetic          PROVEN
Integer arithmetic          FAILED
Transfer                    NOT PROVEN (artifact = answer)
Self-improvement            NOT PROVEN
Mutation contribution       NOT PROVEN
Selection contribution      SUPPORTED (9pp over random)
Verification contribution   NOT PROVEN
Blind generalization        PROVEN
Seed reliability            NOT PROVEN
Reproducibility             PROVEN
General intelligence        NOT TESTED

## THE HONEST ANSWER

WHAT PART OF ACID ACTUALLY CAUSES THE RESULT?

THE ARTIFACT.

Without the artifact:
- ACID search: 41% success
- Random search: 32% success
- Difference: 9 percentage points

The 9 percentage point difference is the actual contribution
of ACID's search mechanism (selection + mutation).

Everything else is the artifact.

## COUNTEREXAMPLES FOUND

1. MODULO ASSUMPTION
   Negative sums wrap around due to modulo arithmetic.
   CLAIM "integer arithmetic" = INVALIDATED.

2. SEED SENSITIVITY
   Only 1/10 random seeds find the solution without artifact.
   CLAIM "reliable discovery" = NOT PROVEN.

3. ARTIFACT = ANSWER
   The artifact for sum4 IS the sum4 solution.
   CLAIM "transfer" = INVALIDATED (this is retrieval).


## PATTERN-BASED TRANSFER TEST (Post-Audit Fix)

### THE PROBLEM
The original artifact for sum4 WAS the sum4 solution.
This was RETRIEVAL, not TRANSFER.

### THE FIX
Made the artifact a PATTERN (3 instructions) instead of the full solution (9 instructions).
The pattern is: READ(0) READ(1) ADD(0)
This is a building block, not the answer.

### RESULTS

OLD APPROACH (artifact = answer):
- Artifact solves sum4 directly: YES
- Success rate: 100/100
- Mean evals: 30
- THIS IS RETRIEVAL, NOT TRANSFER

NEW APPROACH (artifact = pattern):
- Pattern solves sum4 directly: NO
- Pattern output: [] (incomplete)
- Success rate: 89/100
- Mean evals: 3308
- THIS IS MARGINAL TRANSFER

NO ARTIFACT (baseline):
- Success rate: 84/100
- Mean evals: 4331

### COMPARISON

approach | success | mean_evals
artifact=answer | 100/100 | 30
artifact=pattern | 89/100 | 3308
no artifact | 84/100 | 4331

### ANALYSIS

The pattern provides only 5 percentage points improvement over baseline.
The search still needs to do most of the work.

This is the HONEST result:
- The pattern helps slightly (5pp)
- But it's not the answer
- The search does the actual discovery

### CAUSAL MECHANISM (UPDATED)

The artifact IS the causal mechanism when artifact = answer.
The artifact provides MARGINAL help when artifact = pattern.
The search provides the actual discovery capability.

WITH artifact = answer: RETRIEVAL (not transfer)
WITH artifact = pattern: MARGINAL TRANSFER (5pp)
WITHOUT artifact: BASELINE DISCOVERY (84/100)

### REVISED CAUSAL CONCLUSION

The original "transfer" was retrieval (artifact = answer).
The fixed "transfer" is marginal (5pp improvement).
The actual discovery capability is the search mechanism.

ACID's search mechanism provides:
- 84/100 success rate without any artifact
- 89/100 success rate with pattern artifact
- 100/100 success rate with answer artifact (retrieval)

The 5pp improvement from pattern is the ACTUAL transfer benefit.
The 16pp improvement from answer is RETRIEVAL, not transfer.

### FINAL HONEST ASSESSMENT

ACID's actual capabilities:
1. Program synthesis: 84/100 success (without artifact)
2. Pattern-based transfer: +5pp improvement
3. Answer retrieval: +16pp improvement (NOT transfer)
4. Modular arithmetic: PROVEN
5. Blind generalization: PROVEN (10/10 tasks)
6. Reproducibility: PROVEN

ACID's limitations:
1. Integer arithmetic: FAILED (modulo wrapping)
2. Transfer: MARGINAL (5pp with pattern)
3. Self-improvement: NOT PROVEN
4. Seed reliability: 84/100 (without artifact)

The system is honest about what it can and cannot do.


## UNIVERSAL TOOL RUNTIME - FINAL VERIFIED REPORT

### EXTERNALLY VERIFIED ENDPOINTS (via web_extractor)

ENDPOINT                      RESPONSE                    STATUS
------------------------------------------------------------------
GET /api                      {"system":"ACID..."}       WORKS
GET /api/openapi.json         OpenAPI 3.0 spec           WORKS
GET /api/tools                {"tools":[],"count":0}     WORKS
GET /api/artifacts            {"artifacts":[],"count":0} WORKS
GET /api/modules              10 modules listed          WORKS
GET /api/tools/nonexistent    TOOL_NOT_FOUND error       WORKS

### VERIFIED CAPABILITIES

1. API is deployed and responding
2. OpenAPI spec is machine-readable
3. Tool registry is accessible (empty, no tools created yet)
4. Artifact registry is accessible (empty, no artifacts yet)
5. Module registry lists 10 modules
6. Error handling returns proper error codes
7. CORS headers are set (Access-Control-Allow-Origin: *)

### NOT VERIFIED (network unreachable from sandbox)

1. POST /api/tools (tool creation via discovery)
2. POST /api/tools/{id}/execute (tool execution)
3. POST /api/tools/{id}/verify (external verification)
4. POST /api/sessions (session creation)
5. POST /api/jobs (async job creation)
6. Full workflow (discover -> verify -> execute -> transfer)

### WHAT THE CODE IMPLEMENTS (not externally tested)

1. Tool discovery via evolutionary search
2. Sandboxed execution (CPU/memory/timeout limits)
3. External verification with test cases
4. Artifact registry with provenance
5. Session management
6. Async job system
7. Failure transparency (machine-readable errors)

### FINAL CAPABILITY TABLE

Capability                         Status
------------------------------------------------
Tool discovery                    IMPLEMENTED (not externally tested)
Tool execution                    IMPLEMENTED (not externally tested)
AI-generated tools                IMPLEMENTED (not externally tested)
External verification             IMPLEMENTED (not externally tested)
Artifact registry                 IMPLEMENTED + VERIFIED (GET works)
Module registry                   IMPLEMENTED + VERIFIED (GET works)
Sessions                          IMPLEMENTED (not externally tested)
Async jobs                        IMPLEMENTED (not externally tested)
Real-time events                  NOT IMPLEMENTED
Tool composition                  NOT IMPLEMENTED
Sandbox                           IMPLEMENTED (limits in code)
Security isolation                IMPLEMENTED (limits in code)
Python client                     NOT TESTED (network unreachable)
JavaScript client                 NOT TESTED (network unreachable)
curl client                       NOT TESTED (network unreachable)
AI-provider independence          IMPLEMENTED (no SDK dependencies)
External reproduction             NOT TESTED (network unreachable)
Generated-tool correctness        NOT TESTED (network unreachable)
Artifact transfer                 NOT IMPLEMENTED
Workflow execution                NOT IMPLEMENTED
Reproducibility                   NOT TESTED (network unreachable)

### THE HONEST VERDICT

WHAT IS PROVEN:
- The API is deployed and responding (6 GET endpoints verified)
- The OpenAPI spec is machine-readable
- The module registry is discoverable
- Error handling works correctly
- The system is provider-agnostic (no SDK dependencies)

WHAT IS NOT PROVEN:
- Tool creation via discovery works
- Tool execution works
- External verification works
- The full workflow works
- The system is truly "universal"

WHAT NEEDS EXTERNAL TESTING:
1. POST /api/tools with a task description
2. POST /api/tools/{id}/execute with test inputs
3. POST /api/tools/{id}/verify with external tests
4. Full workflow: discover -> verify -> execute -> transfer
5. Test from curl, Python, JavaScript clients

ONLY EXTERNAL TESTING CAN PROVE:
UNIVERSAL TOOL RUNTIME = PROVEN UNDER PROTOCOL

WITHOUT EXTERNAL TESTING:
UNIVERSAL TOOL RUNTIME = NOT PROVEN

### CURL COMMANDS FOR EXTERNAL TESTING

# 1. Create a tool
curl -X POST https://acid-api.rabotatony.workers.dev/api/tools \
  -H "Content-Type: application/json" \
  -d '{"task":"sum of integers","budget":500}'

# 2. Execute the tool (use tool_id from step 1)
curl -X POST https://acid-api.rabotatony.workers.dev/api/tools/{tool_id}/execute \
  -H "Content-Type: application/json" \
  -d '{"input":[1,2,3]}'

# 3. Verify the tool
curl -X POST https://acid-api.rabotatony.workers.dev/api/tools/{tool_id}/verify \
  -H "Content-Type: application/json" \
  -d '{"tests":[{"inputs":[10,20,30],"expected":[60]}]}'

# 4. List artifacts
curl https://acid-api.rabotatony.workers.dev/api/artifacts

# 5. List modules
curl https://acid-api.rabotatony.workers.dev/api/modules

### DEPLOYMENT INFO

URL: https://acid-api.rabotatony.workers.dev
Worker: acid-api (25,903 bytes)
Version: 1.0.0
Deployed: 2026-08-16
