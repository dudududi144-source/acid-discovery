# ACID - Autonomous Computational Intelligence Discovery

A system that discovers, verifies, distills, and transfers computational mechanisms through evolutionary search on a minimal substrate.

## Overview

ACID is a program synthesis system that:
1. Discovers solutions through evolutionary search
2. Verifies solutions independently
3. Distills reusable patterns from successful solutions
4. Transfers knowledge to new tasks
5. Tracks self-improvement over generations

## Substrate: 20 Primitives

| Category | Primitives |
|----------|------------|
| Stack | PUSH, POP, DUP, SWAP |
| Arithmetic | ADD, SUB, MUL, MOD |
| Comparison | GT, LT, EQ |
| Logic | AND, OR, NOT |
| Memory | READ, WRITE, STORE, LOAD |
| Control | JZ, HALT |

## Discovery Engine

- Smart mutation: 3 strategies based on current score
- Crossover: Combines two successful programs
- KB seeding: Uses known solutions as starting points
- History tracking: Records progress for self-improvement

## Deployed

- UI + API: https://acid-api.rabotatony.workers.dev
- Repo: https://github.com/dudududi144-source/acid-discovery

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Web UI |
| /api/status | GET | System health |
| /api/solve | POST | Submit problem for discovery |
| /api/knowledge | GET | List stored artifacts |
| /api/knowledge | POST | Store artifact |
| /api/analytics | GET | Metrics + history |
| /api/transfer | POST | Transfer test |

## Tasks Verified (8/8)

| Task | Description | Method |
|------|-------------|--------|
| sum2 | Sum of 2 inputs | READ + ADD + WRITE |
| sum3 | Sum of 3 inputs | READ + ADD x 2 + WRITE |
| sum4 | Sum of 4 inputs | READ + ADD x 3 + WRITE |
| mul2 | Product of 2 inputs | READ + MUL + WRITE |
| double | Double the input | READ + DUP + ADD + WRITE |
| max2 | Max of 2 inputs | STORE + LOAD + GT + JZ |
| min2 | Min of 2 inputs | STORE + LOAD + LT + JZ |
| abs | Absolute value | STORE + LOAD + LT + SUB + JZ |

## Installation

pip install git+https://github.com/dudududi144-source/acid-discovery.git

## Principles

1. Truth > Appearance
2. Evidence > Claim
3. Execution > Explanation
4. Correct Failure > Fabricated Success
5. Composition > Addition
6. Verification > Trust
7. Distillation > Storage
8. Transfer > Specialization

## License

MIT License
