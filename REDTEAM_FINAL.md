# ACID Extreme Red-Team Report — FINAL

## Date: 2026-08-22
## Method: In-runtime red-team endpoint (GET /api/redteam)
## Total Tests: 27
## Result: 27/27 PASS (after SA-4 fix)

## Bug Found and Fixed

### BUG: SA-4 — Unknown task returns 201 instead of 422

CLAIM: Unknown tasks should return 422 DISCOVERY_FAILED
REQUEST: POST /api/tools {"task":"compute the meaning of life"}
EXPECTED: 422 DISCOVERY_FAILED
ACTUAL (before fix): 201 (tool created with identity program)
ROOT CAUSE: Fallback test case matched identity candidate
FIX: Return 422 DISCOVERY_FAILED for unrecognized tasks
REGRESSION: SA-4 now returns 422 (verified)

## Full Results (27/27 PASS)

### State Machine Tests (7/7)

| ID | Test | Expected | Actual | Pass |
|----|------|----------|--------|------|
| SM-1 | execute nonexistent tool | 404 | 404 | PASS |
| SM-2 | verify nonexistent tool | 404 | 404 | PASS |
| SM-3 | execute twice same input | same output | same | PASS |
| SM-4 | verify twice | same result | same | PASS |
| SM-5 | session delete twice | 204 then 404 | 204 then 404 | PASS |
| SM-6 | job cancel twice | both succeed | 200 then 200 | PASS |
| SM-7 | read deleted session | 404 | 404 | PASS |

### Input Attack Tests (11/11)

| ID | Test | Expected | Actual | Pass |
|----|------|----------|--------|------|
| IA-1 | POST tools empty body | 400 | 400 | PASS |
| IA-2 | POST tools null task | 400 | 400 | PASS |
| IA-3 | POST tools empty string | 400 | 400 | PASS |
| IA-4 | POST tools 10001 chars | 400 | 400 | PASS |
| IA-5 | execute null input | 400 | 400 | PASS |
| IA-6 | execute empty array | 200 | 200 | PASS |
| IA-7 | execute large numbers | 200 | 200 | PASS |
| IA-8 | execute negative numbers | 200 | 200 | PASS |
| IA-9 | execute string in array | 200 or 400 | 200 | PASS |
| IA-10 | verify empty tests | 200 | 200 | PASS |
| IA-11 | verify wrong expected | failed > 0 | 1 | PASS |

### Semantic Tests (4/4)

| ID | Test | Expected | Actual | Pass |
|----|------|----------|--------|------|
| SA-1 | double(7) = 14 | [14] | [14] | PASS |
| SA-2 | add(3,7) = 10 | [10] | [10] | PASS |
| SA-3 | multiply(4,5) = 20 | [20] | [20] | PASS |
| SA-4 | unknown task | 422 | 422 | PASS (after fix) |

### Path Attack Tests (3/3)

| ID | Test | Expected | Actual | Pass |
|----|------|----------|--------|------|
| PA-1 | path traversal in ID | 404 | 404 | PASS |
| PA-2 | very long tool ID | 404 | 404 | PASS |
| PA-3 | special chars in ID | 404 | 404 | PASS |

### Concurrency Tests (2/2)

| ID | Test | Expected | Actual | Pass |
|----|------|----------|--------|------|
| CC-1 | create 5 tools rapidly | 5 | 5 | PASS |
| CC-2 | all tool IDs unique | true | true | PASS |

## Claims Verified

| Claim | Evidence | Verdict |
|-------|----------|---------|
| Tool creation works | SA-1, SA-2, SA-3 create tools | PROVEN |
| Tool execution is correct | double(7)=14, add(3,7)=10, multiply(4,5)=20 | PROVEN |
| Tool verification works | IA-11 detects wrong expected | PROVEN |
| Error handling is correct | IA-1 through IA-5 return 400 | PROVEN |
| State machine is consistent | SM-1 through SM-7 all pass | PROVEN |
| Idempotency works | SM-3, SM-4 same results | PROVEN |
| Session lifecycle works | SM-5, SM-7 correct transitions | PROVEN |
| Job lifecycle works | SM-6 cancel works | PROVEN |
| Path traversal blocked | PA-1, PA-2, PA-3 all 404 | PROVEN |
| Unknown tasks rejected | SA-4 returns 422 | PROVEN (after fix) |
| Concurrent creation works | CC-1, CC-2 all unique | PROVEN |

## Claims NOT Proven

| Claim | Status |
|-------|--------|
| Self-improvement | NOT PROVEN |
| Knowledge transfer | NOT PROVEN |
| Open-ended discovery | NOT PROVEN |
| Frontier expansion | NOT PROVEN |
| Independent verification | NOT PROVEN (same executor) |
| Persistence across cold starts | NOT PROVEN |
| Rate limiting | NOT PROVEN (absent) |
| Authentication | NOT PROVEN (absent) |

## Security Findings

| Area | Finding | Severity |
|------|---------|----------|
| Authentication | NONE | HIGH |
| CORS | * wildcard | HIGH |
| Rate limiting | NONE | MEDIUM |
| Path traversal | BLOCKED | OK |
| Input validation | WORKING | OK |
| Error leakage | NONE | OK |

## Final Scores

| Area | Score |
|------|-------|
| API correctness | 9/10 |
| Security | 3/10 |
| State consistency | 9/10 |
| Execution correctness | 9/10 |
| Verification strength | 6/10 |
| Scientific validity | 4/10 |
| Transfer evidence | 1/10 |
| Reproducibility | 8/10 |
| Observability | 5/10 |
| Production readiness | 3/10 |

## Verdict

The API's core functionality is VERIFIED WORKING.
The state machine is CONSISTENT.
The execution engine is CORRECT for supported tasks.
Error handling is PROPER.
Idempotency is MAINTAINED.
Path attacks are BLOCKED.

The API is NOT production-ready due to:
- No authentication
- No rate limiting
- CORS wide open
- No persistence (in-memory)
- Limited discovery (5 hardcoded candidates)
- No independent verification

The API IS suitable for sandbox/development use.
