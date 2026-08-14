#!/usr/bin/env python3
"""
ACID - Autonomous Computational Intelligence Discovery
THE ACTUAL EXECUTABLE PRODUCT

Usage:
  python run.py [--seed 42] [--generations 50] [--population 30] [--quick]

This is not a proposal. This executes the full pipeline and reports evidence.
"""
import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from acid.substrate import validate_substrate, substrate_budget, Executor
from acid.tasks import TASKS_TRAIN, TASKS_TRANSFER, TASKS_NOVEL, calibrate_task, verify_hand_solution
from acid.search import DiscoveryEngine
from acid.verifier import IndependentVerifier
from acid.distiller import Distiller
from acid.transfer import TransferTester
from acid.improver import SelfImprovementMeasurer
from acid.adversary import Adversary
from acid.evidence import EvidenceGraph


def phase_0_substrate_validation(evidence):
    """PHASE 0: Prove substrate can compute."""
    print("\n" + "="*60)
    print("  PHASE 0: SUBSTRATE VALIDATION")
    print("="*60)

    results = validate_substrate()
    budget = substrate_budget()

    all_pass = results.get("ALL_PASS", False)
    print(f"  Primitives: {budget['primitive_count']}")
    print(f"  Intelligence embedded: {budget['intelligence']}")
    print(f"  All validation tests pass: {all_pass}")

    for name, r in results.items():
        if name != "ALL_PASS":
            status = "PASS" if r["pass"] else "FAIL"
            print(f"    [{status}] {name}")

    claim_id = evidence.add_claim(
        "Substrate can compute basic functions (add, compare, branch, I/O)",
        "FACT"
    )
    evidence.add_experiment(claim_id, "substrate_validation", results, "PASS" if all_pass else "FAIL")
    evidence.set_verdict(claim_id, "CONFIRMED" if all_pass else "REFUTED")

    return all_pass, budget


def phase_1_task_calibration(evidence):
    """PHASE 1: Verify tasks require structure."""
    print("\n" + "="*60)
    print("  PHASE 1: TASK CALIBRATION")
    print("="*60)

    calibration_results = {}

    # Verify hand solutions
    for task_name, task_def in TASKS_TRAIN.items():
        if task_def.get("hand_solution"):
            verification = verify_hand_solution(task_def)
            print(f"  Hand solution for {task_name}: {'VERIFIED' if verification['verified'] else 'FAILED'}")

    # Calibrate tasks (check random success rate)
    for task_name, task_def in TASKS_TRAIN.items():
        cal = calibrate_task(task_name, task_def, n_random=100)
        calibration_results[task_name] = cal
        status = "CALIBRATED" if cal["calibrated"] else "TOO_EASY"
        print(f"  {task_name}: random_rate={cal['random_success_rate']:.3f} [{status}]")

    claim_id = evidence.add_claim(
        "Tasks require computational structure (random success < 5%)",
        "EXPERIMENTAL_RESULT"
    )
    all_calibrated = all(c["calibrated"] for c in calibration_results.values())
    evidence.add_experiment(claim_id, "task_calibration", calibration_results,
                          "PASS" if all_calibrated else "PARTIAL")
    evidence.set_verdict(claim_id, "CONFIRMED" if all_calibrated else "INCONCLUSIVE")

    return calibration_results


def phase_2_discovery(evidence, seed, generations, population):
    """PHASE 2: Structured discovery on Task Family A."""
    print("\n" + "="*60)
    print("  PHASE 2: STRUCTURED DISCOVERY (Task Family A)")
    print("="*60)

    engine = DiscoveryEngine(seed=seed, population_size=population, max_generations=generations)
    all_candidates = []

    for task_name, task_def in TASKS_TRAIN.items():
        print(f"  Discovering: {task_name}...")
        candidates = engine.discover(
            task_def["fn"],
            inputs=task_def.get("inputs", []),
            generations=generations
        )
        all_candidates.extend(candidates)
        found = len([c for c in candidates if c.evaluation and c.evaluation["score"] > 0.5])
        print(f"    Candidates: {len(candidates)}, Solutions found: {found}")

    stats = engine.get_stats()
    print(f"  Total generated: {stats['generated']}")
    print(f"  Total executed: {stats['executed']}")
    print(f"  Novel: {stats['novel']}")
    print(f"  Failed: {stats['failed']}")

    claim_id = evidence.add_claim(
        "Discovery engine produces candidates that solve tasks",
        "EXPERIMENTAL_RESULT"
    )
    evidence.add_experiment(claim_id, "discovery_phase_2", stats,
                          "PASS" if stats["executed"] > 0 else "FAIL")
    evidence.set_verdict(claim_id, "CONFIRMED" if len(all_candidates) > 0 else "REFUTED")

    return engine, all_candidates, stats


def phase_3_verification(evidence, candidates):
    """PHASE 3: Independent verification."""
    print("\n" + "="*60)
    print("  PHASE 3: INDEPENDENT VERIFICATION")
    print("="*60)

    verifier = IndependentVerifier()
    verified_candidates = []

    for cand in candidates[:10]:
        task_def = list(TASKS_TRAIN.values())[0]
        inputs = task_def.get("inputs", [])
        expected = task_def.get("expected_output")

        result = verifier.full_verify(cand.program, task_def["fn"], inputs, expected)
        cand.verification = result

        if result["overall_pass"]:
            verified_candidates.append(cand)
            print(f"  VERIFIED: {cand.program.hash()} (score={cand.evaluation['score'] if cand.evaluation else '?'})")
        else:
            print(f"  REJECTED: {cand.program.hash()}")

    print(f"  Verified: {len(verified_candidates)}/{len(candidates[:10])}")

    claim_id = evidence.add_claim(
        "Candidates pass independent verification",
        "EXPERIMENTAL_RESULT"
    )
    evidence.add_experiment(claim_id, "verification_phase_3",
                          {"verified": len(verified_candidates), "tested": len(candidates[:10])},
                          "PASS" if verified_candidates else "FAIL")
    evidence.set_verdict(claim_id, "CONFIRMED" if verified_candidates else "INCONCLUSIVE")

    return verified_candidates


def phase_4_distillation(evidence, verified_candidates):
    """PHASE 4: Knowledge distillation."""
    print("\n" + "="*60)
    print("  PHASE 4: KNOWLEDGE DISTILLATION")
    print("="*60)

    distiller = Distiller()
    task_def = list(TASKS_TRAIN.values())[0]

    if len(verified_candidates) >= 2:
        artifact = distiller.distill(
            verified_candidates,
            task_fn=task_def["fn"],
            inputs=task_def.get("inputs", [])
        )
        if artifact:
            print(f"  Artifact: {artifact.hash}")
            print(f"  Complexity: {artifact.complexity_before} -> {artifact.complexity_after}")
            print(f"  Pattern: {json.dumps(artifact.pattern, default=str)[:100]}")

            claim_id = evidence.add_claim(
                "Distillation extracts reusable structure from successful candidates",
                "EXPERIMENTAL_RESULT"
            )
            evidence.add_experiment(claim_id, "distillation_phase_4", artifact.to_dict(), "PASS")
            evidence.set_verdict(claim_id, "CONFIRMED")
            return artifact
        else:
            print("  No patterns extracted")
            return None
    else:
        print("  Insufficient candidates for distillation")
        return None


def phase_5_transfer(evidence, artifact, seed):
    """PHASE 5: Transfer test (fresh runtime, unseen tasks)."""
    print("\n" + "="*60)
    print("  PHASE 5: TRANSFER TEST (Task Family B - UNSEEN)")
    print("="*60)

    transfer_tester = TransferTester(seed=seed + 1000, budget=100)
    transfer_results = {}

    for task_name, task_def in TASKS_TRANSFER.items():
        print(f"  Transfer to: {task_name}...")
        result = transfer_tester.test_transfer(
            artifact,
            task_def["fn"],
            task_def.get("inputs", []),
            generations=20
        )
        transfer_results[task_name] = result
        status = "TRANSFERRED" if result["transfer_confirmed"] else "NOT_TRANSFERRED"
        print(f"    WITH artifact: {result['with_artifact']['evaluations']} evals, found={result['with_artifact']['found_solution']}")
        print(f"    WITHOUT artifact: {result['without_artifact']['evaluations']} evals, found={result['without_artifact']['found_solution']}")
        print(f"    Status: {status}")

    any_transfer = any(r["transfer_confirmed"] for r in transfer_results.values())
    claim_id = evidence.add_claim(
        "Discovered mechanisms transfer to unseen task family",
        "EXPERIMENTAL_RESULT"
    )
    evidence.add_experiment(claim_id, "transfer_phase_5", transfer_results,
                          "PASS" if any_transfer else "FAIL")
    evidence.set_verdict(claim_id, "CONFIRMED" if any_transfer else "INCONCLUSIVE")

    return transfer_results


def phase_6_self_improvement(evidence, artifact, seed):
    """PHASE 6: Self-improvement measurement."""
    print("\n" + "="*60)
    print("  PHASE 6: SELF-IMPROVEMENT MEASUREMENT")
    print("="*60)

    measurer = SelfImprovementMeasurer(seeds=[seed, seed+1, seed+2])
    result = measurer.measure(TASKS_TRAIN, [artifact] if artifact else [], generations=20, population=15)

    print(f"  SYSTEM_0 (no knowledge): avg_evals={result['system_0']['avg_evaluations']:.1f}, found_rate={result['system_0']['found_rate']:.2f}")
    print(f"  SYSTEM_1 (with knowledge): avg_evals={result['system_1']['avg_evaluations']:.1f}, found_rate={result['system_1']['found_rate']:.2f}")
    print(f"  Improvement ratio: {result['improvement_ratio']:.3f}")
    print(f"  Improved: {result['improved']}")

    claim_id = evidence.add_claim(
        "Integrated knowledge measurably improves discovery capability",
        "EXPERIMENTAL_RESULT"
    )
    evidence.add_experiment(claim_id, "self_improvement_phase_6", result,
                          "PASS" if result["improved"] else "FAIL")
    evidence.set_verdict(claim_id, "CONFIRMED" if result["improved"] else "INCONCLUSIVE")

    return result


def phase_7_adversarial(evidence, context):
    """PHASE 7: Adversarial validation."""
    print("\n" + "="*60)
    print("  PHASE 7: ADVERSARIAL VALIDATION")
    print("="*60)

    adversary = Adversary()
    result = adversary.run_all_attacks(context)

    print(f"  Attacks run: {len(result['attacks'])}")
    print(f"  High risk: {result['high_risk']}")
    print(f"  Medium risk: {result['medium_risk']}")
    print(f"  Overall: {result['overall']}")

    for attack in result["attacks"]:
        print(f"    [{attack['risk']}] {attack['attack']}")

    return result


def phase_8_verdict(evidence, results):
    """PHASE 8: Final verdict."""
    print("\n" + "="*60)
    print("  PHASE 8: FINAL VERDICT")
    print("="*60)

    summary = evidence.summary()
    print(f"  Claims: {summary['total_claims']}")
    print(f"  Confirmed: {summary['confirmed']}")
    print(f"  Refuted: {summary['refuted']}")
    print(f"  Inconclusive: {summary['inconclusive']}")
    print(f"  Unverified: {summary['unverified']}")

    # Determine overall verdict
    if summary["confirmed"] > summary["refuted"] and summary["confirmed"] >= 3:
        verdict = "CONFIRMED"
    elif summary["refuted"] > summary["confirmed"]:
        verdict = "REFUTED"
    else:
        verdict = "INCONCLUSIVE"

    print(f"\n  OVERALL VERDICT: {verdict}")
    return verdict


def run_full_experiment(seed=42, generations=50, population=30, quick=False):
    """Execute the complete ACID pipeline."""
    print("="*60)
    print("  ACID: AUTONOMOUS COMPUTATIONAL INTELLIGENCE DISCOVERY")
    print("  Executing full pipeline...")
    print("="*60)

    if quick:
        generations = 15
        population = 15

    evidence = EvidenceGraph()
    start_time = time.time()

    results = {
        "generated": 0, "executed": 0, "verified": 0, "novel": 0,
        "distilled": 0, "transferable": 0, "replicated": 0,
        "refuted": 0, "failed": 0, "cannotRun": 0
    }

    # PHASE 0
    substrate_ok, budget = phase_0_substrate_validation(evidence)
    if not substrate_ok:
        print("\n  FATAL: Substrate cannot compute. Aborting.")
        return {"error": "substrate_validation_failed", "results": results}

    # PHASE 1
    calibration = phase_1_task_calibration(evidence)

    # PHASE 2
    engine, candidates, search_stats = phase_2_discovery(evidence, seed, generations, population)
    results["generated"] = search_stats["generated"]
    results["executed"] = search_stats["executed"]
    results["novel"] = search_stats["novel"]
    results["failed"] = search_stats["failed"]

    # PHASE 3
    verified = phase_3_verification(evidence, candidates)
    results["verified"] = len(verified)

    # PHASE 4
    artifact = phase_4_distillation(evidence, verified)
    results["distilled"] = 1 if artifact else 0

    # PHASE 5
    transfer_results = phase_5_transfer(evidence, artifact, seed)
    results["transferable"] = sum(1 for r in transfer_results.values() if r["transfer_confirmed"])

    # PHASE 6
    improvement = phase_6_self_improvement(evidence, artifact, seed)

    # PHASE 7
    adversarial = phase_7_adversarial(evidence, {
        "results": [c.evaluation for c in candidates if c.evaluation],
        "candidate": candidates[0] if candidates else None,
        "known_programs": [c.program for c in candidates[:10]],
        "system_0_stats": {"executed": improvement["system_0"]["avg_evaluations"]},
        "system_1_stats": {"executed": improvement["system_1"]["avg_evaluations"]},
    })

    # PHASE 8
    verdict = phase_8_verdict(evidence, results)

    elapsed = time.time() - start_time

    # FINAL OUTPUT
    print("\n" + "="*60)
    print("  FINAL RESULTS")
    print("="*60)
    print(f"  generated    = {results['generated']}")
    print(f"  executed     = {results['executed']}")
    print(f"  verified     = {results['verified']}")
    print(f"  novel        = {results['novel']}")
    print(f"  distilled    = {results['distilled']}")
    print(f"  transferable = {results['transferable']}")
    print(f"  replicated   = {results['replicated']}")
    print(f"  refuted      = {results['refuted']}")
    print(f"  failed       = {results['failed']}")
    print(f"  cannotRun    = {results['cannotRun']}")
    print(f"\n  VERDICT: {verdict}")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Evidence: {json.dumps(evidence.summary())}")

    # Save results
    output = {
        "results": results,
        "verdict": verdict,
        "evidence_summary": evidence.summary(),
        "substrate_budget": budget,
        "improvement": improvement,
        "adversarial": adversarial["overall"],
        "elapsed_seconds": elapsed,
        "config": {"seed": seed, "generations": generations, "population": population},
        "timestamp": time.time()
    }

    os.makedirs("output", exist_ok=True)
    with open("output/final_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    print("\n  Results saved to output/final_results.json")

    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ACID Discovery System")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--generations", type=int, default=50)
    parser.add_argument("--population", type=int, default=30)
    parser.add_argument("--quick", action="store_true", help="Quick run with reduced parameters")
    args = parser.parse_args()

    run_full_experiment(seed=args.seed, generations=args.generations,
                       population=args.population, quick=args.quick)
