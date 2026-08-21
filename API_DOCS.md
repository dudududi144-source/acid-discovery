# ACID API Documentation v24.1.0

SOURCE OF TRUTH: /api/openapi.json
Last synced: 2026-08-21

## Base URL

https://acid-api.rabotatony.workers.dev

## Authentication

NONE. The API is fully public. No API key required.

## Endpoints

### Discovery
- GET / — API info + discoverability
- GET /api — System info + endpoint list
- GET /api/health — Health check
- GET /api/openapi.json — OpenAPI 3.0.0 spec
- GET /docs — Docs alias

### Tools
- GET /api/tools — List all tools
- POST /api/tools — Create tool via discovery
- GET /api/tools/{tool_id} — Get tool details
- POST /api/tools/{tool_id}/execute — Execute a tool
- POST /api/tools/{tool_id}/verify — Verify a tool

### Artifacts
- GET /api/artifacts — List all artifacts
- GET /api/artifacts/{artifact_id} — Get artifact details

### Sessions
- GET /api/sessions — List sessions
- POST /api/sessions — Create session
- GET /api/sessions/{session_id} — Get session
- DELETE /api/sessions/{session_id} — Delete session

### Jobs
- GET /api/jobs — List jobs
- POST /api/jobs — Create async job
- GET /api/jobs/{job_id} — Get job status
- POST /api/jobs/{job_id}/cancel — Cancel job

### Modules
- GET /api/modules — List modules
- GET /api/modules/{module_name} — Get module details

## Error Codes
- INVALID_JSON (400)
- MISSING_TASK (400)
- TASK_TOO_LONG (400)
- MISSING_INPUT (400)
- MISSING_TESTS (400)
- TOOL_NOT_FOUND (404)
- ARTIFACT_NOT_FOUND (404)
- SESSION_NOT_FOUND (404)
- JOB_NOT_FOUND (404)
- MODULE_NOT_FOUND (404)
- DISCOVERY_FAILED (422)
- NOT_FOUND (404)

## Known Limitations
- No persistence: in-memory only, lost on cold start
- No auth: fully public, no rate limiting
- Discovery limited: 5 hardcoded candidates
- Jobs complete synchronously
- CORS: * (wide open)

## Removed Endpoints (were in old API_DOCS.md, do NOT exist)
- /api/status — REMOVED (use /api/health)
- /api/solve — REMOVED (use /api/tools)
- /api/knowledge — REMOVED
- /api/transfer — REMOVED
- /api/evidence — REMOVED
