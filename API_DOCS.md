# ACID API Documentation

## Base URL

https://acid-api.rabotatony.workers.dev

## Endpoints

### GET /api/status
Returns system health and metrics.

Response:
- system: "online"
- version: "3.0.0"
- kb_size: number of artifacts
- solves: total solves
- success_rate: percentage
- avg_time: average solve time
- components: status of each component

### POST /api/solve
Submit a problem for discovery.

Request body:
- problem: string (problem description)
- inputs: array (input values)
- expected: array (expected output)

Response (solved):
- solve_id: string
- status: "solved"
- time: seconds
- evals: number of evaluations
- gen: generation found
- program: the discovered program
- verification: verification results
- artifact: artifact hash

Response (not found):
- solve_id: string
- status: "not_found"
- evals: number of evaluations
- bestScore: best score achieved

### GET /api/stream
SSE real-time stream.

Events:
- connected: Client connected
- solve_started: Discovery started
- discovery_progress: Generation progress
- solve_complete: Solution found
- solve_failed: Discovery failed
- artifact_stored: Artifact stored in KB
- transfer_complete: Transfer completed
- heartbeat: Keep-alive

### GET /api/knowledge
List all artifacts.

Response:
- count: number of artifacts
- artifacts: array of artifacts

### POST /api/knowledge
Store an artifact.

Request body:
- hash: artifact hash
- instructions: program instructions
- constants: program constants
- task: task description

### GET /api/knowledge/:hash
Get artifact with version history.

Response:
- current: current artifact
- versions: number of versions
- history: version history

### GET /api/analytics
Get metrics and history.

Response:
- solves: total solves
- successes: successful solves
- failures: failed solves
- success_rate: success rate
- avg_time: average time
- total_evals: total evaluations
- kb_size: knowledge base size
- history: recent history

### POST /api/transfer
Run transfer test.

Request body:
- source: source artifact hash
- target: target task description
- inputs: input values
- expected: expected output

Response:
- source: source artifact hash
- target: target task
- found: whether solution was found
- evals: number of evaluations
- effective: whether transfer was effective

### GET /api/evidence
Get evidence log.

Response:
- claims: array of claims
- message: status message

## Error Responses

All errors return JSON with an "error" field.

## Notes

- No rate limiting currently enforced
- No authentication currently required
- Consider adding both for production use
