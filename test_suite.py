#!/usr/bin/env python3
"""
ACID TEST SUITE
Unit tests, integration tests, property tests, determinism tests.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from acid.substrate import Program, Executor, validate_substrate, PRIMITIVES
from acid.search import DiscoveryEngine, random_program, mutate_program, crossover
from acid.verifier import IndependentVerifier
from acid.distiller import Distiller
from acid.evidence import EvidenceGraph
import random


def test_substrate_primitives():
    """Test: substrate has exactly the declared primitives."""
    assert len(PRIMITIVES) == 19, f"Expected 19 primitives, got {len(PRIMITIVES)}"
    print("  [PASS] substrate_primitives")


def test_substrate_validation():
    """Test: substrate self-validation passes."""
    results = validate_substrate()
    assert results["ALL_PASS"], f"Substrate validation failed: {results}"
    print("  [PASS] substrate_validation")


def test_executor_determinism():
    """Test: same program + same input = same output."""
    ex = Executor()
    prog = Program([("PUSH", 0), ("WRITE", 0), ("HALT", 0)], constants=[42])
    r1 = ex.execute(prog, inputs=[])
    r2 = ex.execute(prog, inputs=[])
    assert r1["outputs"] == r2["outputs"], "Non-deterministic execution"
    print("  [PASS] executor_determinism")


def test_executor_bounds():
    """Test: executor respects step limits."""
    ex = Executor(max_steps=100)
    # Infinite loop program
    prog = Program([("JZ", 0), ("HALT", 0)], constants=[])
    result = ex.execute(prog, inputs=[0])
    assert result["steps"] <= 100, f"Exceeded step limit: {result['steps']}"
    print("  [PASS] executor_bounds")


def test_random_program_generation():
    """Test: random programs are generated within bounds."""
    rng = random.Random(42)
    for _ in range(50):
        prog = random_program(rng, max_len=50)
        assert len(prog) <= 50, f"Program too long: {len(prog)}"
        assert len(prog) >= 5, f"Program too short: {len(prog)}"
    print("  [PASS] random_program_generation")


def test_mutation_preserves_validity():
    """Test: mutation produces valid programs."""
    rng = random.Random(42)
    prog = random_program(rng, max_len=30)
    for _ in range(20):
        mutated, muts = mutate_program(prog, rng)
        assert len(mutated) > 0, "Mutation produced empty program"
        for op, arg in mutated.instructions:
            assert op in PRIMITIVES + ["HALT"], f"Invalid op: {op}"
    print("  [PASS] mutation_preserves_validity")


def test_crossover():
    """Test: crossover produces valid programs."""
    rng = random.Random(42)
    p1 = random_program(rng, max_len=20)
    p2 = random_program(rng, max_len=20)
    child = crossover(p1, p2, rng)
    assert len(child) > 0, "Crossover produced empty program"
    print("  [PASS] crossover")


def test_verifier_basic():
    """Test: verifier correctly identifies passing/failing programs."""
    verifier = IndependentVerifier()
    # Program that outputs 42
    prog = Program([("PUSH", 0), ("WRITE", 0), ("HALT", 0)], constants=[42])
    result = verifier.verify(prog, [([], [42])])
    assert result["verified"], "Verifier should pass correct program"

    # Program that outputs 99 (wrong)
    prog2 = Program([("PUSH", 0), ("WRITE", 0), ("HALT", 0)], constants=[99])
    result2 = verifier.verify(prog2, [([], [42])])
    assert not result2["verified"], "Verifier should fail incorrect program"
    print("  [PASS] verifier_basic")


def test_verifier_determinism():
    """Test: verifier checks determinism."""
    verifier = IndependentVerifier()
    prog = Program([("PUSH", 0), ("WRITE", 0), ("HALT", 0)], constants=[7])
    result = verifier.verify_determinism(prog, [], runs=5)
    assert result["deterministic"], "Deterministic program flagged as non-deterministic"
    print("  [PASS] verifier_determinism")


def test_discovery_engine():
    """Test: discovery engine produces candidates."""
    engine = DiscoveryEngine(seed=42, population_size=10, max_generations=5)
    task_fn = lambda result: 1.0 if result["outputs"] else 0.0
    candidates = engine.discover(task_fn, inputs=[], generations=5)
    assert engine.stats["generated"] > 0, "No programs generated"
    assert engine.stats["executed"] > 0, "No programs executed"
    print("  [PASS] discovery_engine")


def test_evidence_graph():
    """Test: evidence graph tracks claims and verdicts."""
    eg = EvidenceGraph()
    claim_id = eg.add_claim("Test claim", "EXPERIMENTAL_RESULT")
    exp_id = eg.add_experiment(claim_id, "test experiment", {"data": 1}, "PASS")
    eg.set_verdict(claim_id, "CONFIRMED")

    summary = eg.summary()
    assert summary["total_claims"] == 1
    assert summary["confirmed"] == 1
    assert summary["total_experiments"] == 1
    print("  [PASS] evidence_graph")


def test_distiller():
    """Test: distiller extracts patterns from candidates."""
    from acid.search import Candidate
    rng = random.Random(42)
    programs = [random_program(rng, max_len=20) for _ in range(5)]
    candidates = [Candidate(p) for p in programs]

    distiller = Distiller()
    artifact = distiller.distill(candidates)
    # May or may not find patterns, but should not crash
    print("  [PASS] distiller (no crash)")


def run_all_tests():
    print("\n" + "="*50)
    print("  ACID TEST SUITE")
    print("="*50)

    tests = [
        test_substrate_primitives,
        test_substrate_validation,
        test_executor_determinism,
        test_executor_bounds,
        test_random_program_generation,
        test_mutation_preserves_validity,
        test_crossover,
        test_verifier_basic,
        test_verifier_determinism,
        test_discovery_engine,
        test_evidence_graph,
        test_distiller,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
