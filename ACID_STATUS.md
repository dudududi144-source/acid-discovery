# ACID STATUS

## System: Modular Program Search API (formerly "Universal Tool Runtime")
## Version: 24.1.0
## Last Updated: 2026-08-21

## NAMING CORRECTION (from roast)

OLD: "ACID Universal Tool Runtime"
NEW: "ACID Modular Program Search API"

The word "Universal" was misleading. The system searches a space of
5 hardcoded candidates on a 14-primitive modular VM. It is not universal.

## API STATUS: OPERATIONAL

All GET endpoints verified:
- /api/health → healthy
- /api → system info
- /api/tools → empty list
- /api/artifacts → empty list
- /api/sessions → empty list
- /api/jobs → empty list
- /api/modules → 2 modules
- /api/modules/substrate → 14 primitives
- /api/modules/search → config
- /api/openapi.json → OpenAPI 3.0.0

POST endpoints deployed but not externally verified.

## CLAIMS STATUS (from roast)

RETRACTED:
- "Universal Tool Runtime" → "Modular Program Search API"
- "Autonomous discovery" → "5-candidate lookup"
- "Knowledge transfer" → "Retrieval with search prior"
- "Independent verification" → "Same interpreter, stricter budget"
- "Integer arithmetic" → "Bounded modular arithmetic"
- "Self-improvement" → NOT PROVEN
- "Frontier expansion" → NOT PROVEN
- "Open-ended discovery" → NOT PROVEN

REAL:
- Stack-based VM with 14 primitives
- Evolutionary search over program space
- API for creating/executing/verifying programs
- Health check and module introspection

## KNOWN BUGS (from roast)

1. crossover() defined twice → TypeError
2. Timeout flag mismatch (halted vs timed_out)
3. Score checks only first element
4. full_verify accepts any output when expected=None
5. Transfer artifact injection is pass
6. LOOP in Verifier but not Executor
7. Novelty detector trivial (first 10 = novel)
8. Provenance always "source=random"

See BUGFIXES.md for details.

## ROAST SCORE ACCEPTED

| Area | Score |
|------|-------|
| API discoverability | 8/10 |
| API surface design | 6/10 |
| Documentation consistency | 3/10 → FIXED |
| Substrate clarity | 8/10 |
| Search implementation | 5/10 |
| Verification | 4/10 |
| Transfer methodology | 3/10 |
| Self-improvement evidence | 3/10 |
| Scientific honesty | 8/10 |
| Claims vs evidence | 4/10 |
| Production readiness | 2-3/10 |

## VERDICT

The roast is accurate. The fixes are documented.
The claims are retracted. The system is honest.
The core (program search on modular VM) is real.
Everything else needs external benchmarks to prove.
