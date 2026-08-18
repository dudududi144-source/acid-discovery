#!/usr/bin/env python3
"""
ACID CAPABILITY AMPLIFICATION BENCHMARK
========================================

This script runs the full capability amplification experiment.
It requires access to the ACID API (POST endpoints).

Usage:
    python benchmark.py --base-url https://acid-api.rabotatony.workers.dev

Requirements:
    pip install httpx

Conditions:
    A = MODEL ONLY (no ACID)
    B = MODEL + ACID
    C = MODEL + ACID + PROCEDURAL MEMORY
    D = MODEL + ACID + PROCEDURAL MEMORY + TOOL COMPOSITION

NOTE: This script CANNOT be run from the ACID development sandbox.
It must be run from an external environment with network access.
"""

import httpx
import json
import time
import random
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="ACID Capability Amplification Benchmark")
    parser.add_argument("--base-url", default="https://acid-api.rabotatony.workers.dev")
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--tasks", type=int, default=30)
    return parser.parse_args()

def api_call(base_url, method, path, body=None, timeout=60):
    """Make an API call to ACID."""
    url = base_url + path
    headers = {"Content-Type": "application/json"}
    
    if method == "GET":
        resp = httpx.get(url, headers=headers, timeout=timeout)
    elif method == "POST":
        resp = httpx.post(url, json=body, headers=headers, timeout=timeout)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    try:
        return {"status": resp.status_code, "json": resp.json(), "time": resp.elapsed.total_seconds()}
    except:
        return {"status": resp.status_code, "json": None, "time": resp.elapsed.total_seconds()}

def run_condition_a(task, seeds):
    """Condition A: MODEL ONLY (baseline - no ACID)."""
    # In a real experiment, this would be the AI model trying to solve
    # the task without any tool access. For this benchmark, we simulate
    # the baseline as "no solution found" since the model cannot execute
    # substrate programs without ACID.
    results = []
    for seed in range(seeds):
        results.append({
            "seed": seed,
            "success": False,
            "heldout_correct": 0,
            "heldout_total": 1000,
            "adversarial_correct": 0,
            "evaluations": 0,
            "time": 0,
            "note": "MODEL_ONLY cannot execute substrate programs"
        })
    return results

def run_condition_b(base_url, task, seeds):
    """Condition B: MODEL + ACID."""
    results = []
    for seed in range(seeds):
        start = time.time()
        
        # Step 1: Create tool
        create_resp = api_call(base_url, "POST", "/api/tools", {
            "task": task["spec"],
            "input_schema": {
                "type": "array",
                "items": [{"type": "integer"}] * task["input_len"]
            },
            "output_schema": {
                "type": "array",
                "items": [{"type": "integer"}]
            },
            "budget": 500
        })
        
        if create_resp["status"] != 201:
            results.append({
                "seed": seed,
                "success": False,
                "error": create_resp["json"],
                "time": time.time() - start
            })
            continue
        
        tool_id = create_resp["json"]["tool_id"]
        
        # Step 2: Execute on held-out cases
        held_correct = 0
        for case in task["held_out"][:100]:  # First 100 for speed
            exec_resp = api_call(base_url, "POST", f"/api/tools/{tool_id}/execute", {
                "input": case["inputs"],
                "timeout_ms": 5000
            })
            if exec_resp["status"] == 200 and exec_resp["json"]:
                output = exec_resp["json"].get("output", {}).get("values", [])
                if output == case["expected"]:
                    held_correct += 1
        
        # Step 3: Verify with adversarial cases
        verify_resp = api_call(base_url, "POST", f"/api/tools/{tool_id}/verify", {
            "tests": task["adversarial"][:100]
        })
        
        adv_correct = verify_resp["json"].get("passed", 0) if verify_resp["json"] else 0
        
        results.append({
            "seed": seed,
            "success": held_correct > 50,
            "tool_id": tool_id,
            "heldout_correct": held_correct,
            "heldout_total": 100,
            "adversarial_correct": adv_correct,
            "adversarial_total": 100,
            "time": time.time() - start
        })
    
    return results

def main():
    args = parse_args()
    base_url = args.base_url
    seeds = args.seeds
    
    print("ACID CAPABILITY AMPLIFICATION BENCHMARK")
    print("="*70)
    print(f"BASE URL: {base_url}")
    print(f"SEEDS: {seeds}")
    print()
    
    # Load tasks (embedded in this script)
    # In production, these would be loaded from a separate file
    
    print("PHASE 1: Testing API connectivity...")
    resp = api_call(base_url, "GET", "/api")
    if resp["status"] != 200:
        print("FATAL: Cannot reach ACID API")
        sys.exit(1)
    print(f"  API reachable: {resp['json']}")
    
    print()
    print("PHASE 2: Running Condition A (MODEL ONLY)...")
    # This would be run with actual AI model in production
    
    print()
    print("PHASE 3: Running Condition B (MODEL + ACID)...")
    # This requires POST access to the API
    
    print()
    print("NOTE: This benchmark requires POST access to the ACID API.")
    print("If POST is not available, the experiment cannot be run.")
    print()
    print("CAPABILITY AMPLIFICATION = NOT PROVEN (pending execution)")

if __name__ == "__main__":
    main()
