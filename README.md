# ACID - Autonomous Computational Intelligence Discovery

## The Research Question

Can a deliberately constrained computational substrate, through structured
search and observation, discover mechanisms not explicitly supplied, verify
them independently, distill them into reusable knowledge, and thereby
measurably improve future discovery capability?

## What This Is

An executable product. Not a proposal. Not a roadmap.
Runs the full 8-phase pipeline and reports evidence-backed verdicts.

## Structure

- acid/substrate.py - 19 primitives, self-validating, no intelligence
- acid/tasks.py - Calibrated task families (TRAIN/TRANSFER/NOVEL)
- acid/search.py - Structured discovery (observe-hypothesize-construct)
- acid/verifier.py - Independent adversarial verification
- acid/distiller.py - Knowledge distillation (structural extraction)
- acid/transfer.py - Transfer testing (fresh runtime)
- acid/improver.py - Self-improvement measurement
- acid/adversary.py - Adversarial self-validation
- acid/evidence.py - Evidence graph (claims-experiments-verdicts)
- run.py - THE EXECUTABLE
- test_suite.py - 12 tests

## Usage

python test_suite.py
python run.py --quick
python run.py --seed 42 --generations 50 --population 30

## Phases

0. Substrate Validation (prove it can compute)
1. Task Calibration (verify tasks require structure)
2. Structured Discovery (not just random mutation)
3. Independent Verification (adversarial, property-based)
4. Knowledge Distillation (structural extraction)
5. Transfer Test (fresh runtime, unseen tasks)
6. Self-Improvement (SYSTEM_0 vs SYSTEM_1)
7. Adversarial Validation (attack every result)
8. Final Verdict (CONFIRMED/REFUTED/INCONCLUSIVE)

## Operating Law

TRUTH > APPEARANCE
EVIDENCE > CLAIM
EXECUTION > EXPLANATION
CORRECT FAILURE > FABRICATED SUCCESS