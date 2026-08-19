# Breakthrough Tools Infrastructure

## The Moat

A technological moat is created by the combination of three things
that cannot be replicated without them:

1. Proprietary fitness function - Only you know what "good" means
2. Proprietary data - Only you have the history/context/labels
3. Domain-specific primitives - Operations meaningful only in your domain

The algorithm itself (genetic programming, evolution, LLM) is commodity.
Everyone can run evolution. The moat is in what you feed it and how
you evaluate - not in the search engine.

## Why ACID Does Not Create a Moat

Even if ACID worked perfectly, its output would not create a moat
because it outputs a function that matches the examples you passed.
Anyone with the same examples gets the same result.

The "magic" of breakthrough is not in the search engine, but
in what is defined as "good".

## Where Breakthroughs Actually Come From

1. Optimization on proprietary cost function (strongest moat)
   - Tool: nevergrad / optuna / DEAP (Python, mature, supported)
   - Moat: Your cost function - only you know what it is

2. LLM combining proprietary knowledge + your search strategy
   - Tool: LLM with proprietary system prompt + retrieval on your data
   - Moat: The prompt, retrieval, and tool definitions

3. Pattern discovery on your data
   - Tool: LLM for planning + optimization library for parameter tuning
   - Moat: Your data and evaluation

4. Simulation + search on top of it
   - Tool: Your simulation + nevergrad/optuna
   - Moat: The simulation itself - it is your proprietary code

## The Discovery Engine

The discovery_engine.py module provides:
- DiscoveryEngine class: takes fitness, primitives, budget
- FitnessFunction class: proprietary fitness function
- Primitive class: domain-specific primitive operation
- DiscoveryResult class: result of a discovery run

Usage:
    from discovery_engine import DiscoveryEngine, FitnessFunction, Primitive
    
    primitives = [Primitive("sma", 2, "Simple moving average")]
    fitness = FitnessFunction("sharpe", "Sharpe ratio", evaluate_fn)
    engine = DiscoveryEngine(fitness, primitives, budget=10000)
    result = engine.discover(seed=42)

## Architecture

mini-services/discovery-engine/
  discovery_engine.py    - Core discovery engine
  fitness_functions/     - Proprietary fitness functions
  primitives/            - Domain-specific primitives
  storage/               - Prisma schema for results

ui/                      - Next.js UI
  pages/                 - Dashboard, discovery runs, results
  components/            - Convergence curves, result cards

## Getting Started

1. Define your proprietary fitness function
2. Define your domain-specific primitives
3. Run discovery with optuna/nevergrad
4. Store results in Prisma (your DB, not third-party)
5. Monitor convergence in Next.js UI

The moat is in steps 1-2. Steps 3-5 are infrastructure.
