# ACID System Design

## Architecture

UI (Pages) -> API Worker (Discovery) -> Knowledge Base
                    |
                    v
             Substrate Executor (18 prims)
                    |
                    v
             Verification Pipeline (5 tests)
                    |
                    v
             Distillation Pipeline
                    |
                    v
             Transfer Engine

## Components

### 1. Substrate Executor
- 18 primitives: PUSH, POP, DUP, SWAP, ADD, SUB, MUL, MOD, GT, LT, EQ, AND, OR, NOT, JZ, READ, WRITE, HALT
- Bounded execution (10,000 steps max)
- Deterministic (same input -> same output)
- No side effects

### 2. Discovery Engine
- Evolutionary search (mutation + selection)
- Seeded from knowledge base
- Adaptive budget based on task difficulty
- Real-time progress via SSE

### 3. Verification Pipeline
- Functional test (primary input)
- Multi-input test (10 random inputs)
- Determinism test (5 runs)
- Resource test (step limit)
- Adversarial test (edge cases)

### 4. Knowledge Base
- Artifact storage (hash-addressed)
- Version tracking (full history)
- Usage metrics (success rate)
- Retrieval by task type

### 5. Transfer Engine
- Source -> Target transfer
- Effectiveness measurement
- Speedup calculation

### 6. Feedback Loop
- After solve: update KB, metrics
- After failure: adjust budget
- Knowledge growth tracking

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/status | GET | System health + metrics |
| /api/solve | POST | Submit problem, run discovery |
| /api/stream | GET | SSE real-time stream |
| /api/knowledge | GET | List artifacts |
| /api/knowledge | POST | Store artifact |
| /api/knowledge/:hash | GET | Get artifact + versions |
| /api/analytics | GET | Metrics + history |
| /api/transfer | POST | Run transfer test |
| /api/evidence | GET | Evidence log |

## Data Flow

Problem -> Discovery -> Verification -> Distillation -> Knowledge Base
                                                            |
                                                            v
Future Problem <- Seeded Search <- Knowledge Retrieval <- Transfer

## Validation Strategy

1. Unit tests: Each component in isolation
2. Integration tests: Full pipeline end-to-end
3. Property tests: Invariants maintained
4. Adversarial tests: Edge cases and attacks
5. Performance tests: Time and resource limits

## Deployment

- UI: Cloudflare Pages (acid-ui.pages.dev)
- API: Cloudflare Workers (acid-api.rabotatony.workers.dev)
- Repo: GitHub (dudududi144-source/acid-discovery)

## Principles

1. Truth > Appearance
2. Evidence > Claim
3. Execution > Explanation
4. Correct Failure > Fabricated Success
5. Composition > Addition
6. Verification > Trust
7. Distillation > Storage
8. Transfer > Specialization
