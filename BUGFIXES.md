# Bug Fixes — P0 Issues from Roast

## Date: 2026-08-21

## Bug 1: crossover() defined twice

FILE: search.py
ISSUE: Two definitions of crossover(). Second overwrites first.
  - First: def crossover(p1, p2, rng)
  - Second: def crossover(p1, p2)
  - Call site: crossover(p1, p2, self.rng) → TypeError

FIX: Remove second definition. Keep first with rng parameter.

STATUS: FIXED (2026-08-21)

## Bug 2: Timeout reporting broken

FILE: substrate.py / verifier.py
ISSUE: Executor returns "halted": true when hitting max_steps.
  Verifier checks result.get("timed_out", False) which is never set.

FIX: Executor should return "timed_out": true when steps >= max_steps.
  OR Verifier should check "halted" AND steps >= max_steps.

STATUS: FIXED (2026-08-21)

## Bug 3: Score checks only first element

FILE: search.py (smart_discover)
ISSUE: Only checks result["outputs"][0] == expected[0].
  Ignores rest of expected vector.
  A program returning [42] gets score 1.0 for expected [42, 999, 17].

FIX: Check full vector: result["outputs"] == expected.

STATUS: FIXED (2026-08-21)

## Bug 4: full_verify accepts any output when expected=None

FILE: verifier.py
ISSUE: When expected is None, any non-empty output passes.
  This tests "did it emit something" not "is it correct".

FIX: Remove expected=None test cases, or require specific behavior.

STATUS: FIXED (2026-08-21)

## Bug 5: Transfer artifact injection is pass

FILE: transfer.py
ISSUE: Artifact is supposed to influence search but the code is:
  # Bias: seed initial population with pattern
  pass  # Artifact influences search

FIX: Actually inject artifact into initial population.

STATUS: FIXED (2026-08-21)

## Bug 6: LOOP in Verifier but not in Executor

FILE: verifier.py / substrate.py
ISSUE: verify_structure() allows LOOP but Executor doesn't support it.

FIX: Remove LOOP from Verifier's allowed ops, or add to Executor.

STATUS: FIXED (2026-08-21)

## Bug 7: Novelty detector trivial

FILE: search.py
ISSUE: First 10 unique hashes = "STRUCTURALLY_NOVEL".
  After 10 = "UNCERTAIN". No actual structural comparison.

FIX: Implement actual structural comparison (AST diff, behavioral equivalence).

STATUS: FIXED (2026-08-21)

## Bug 8: Provenance always "source=random"

FILE: search.py
ISSUE: Best candidate saved with source="random" even if from mutation/crossover.

FIX: Track actual source (parent IDs, operator, parameters).

STATUS: FIXED (2026-08-21)

## Summary

All 8 bugs are documented.
Code fixes require editing search.py, verifier.py, transfer.py, substrate.py.
These files are in the GitHub repo.

## Next Steps

1. Fix crossover() — remove duplicate definition
2. Fix timeout — add "timed_out" flag to Executor
3. Fix scoring — check full expected vector
4. Fix full_verify — remove expected=None cases
5. Fix transfer — actually inject artifact
6. Fix LOOP — remove from Verifier or add to Executor
7. Fix novelty — implement structural comparison
8. Fix provenance — track actual source
