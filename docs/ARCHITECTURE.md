# TrustGuard AI — Architecture

Status: **foundation milestone**. Runtime behaviour is limited to configuration, a health API, and a dashboard shell.

## Design principles

1. **Separation of concerns** — HTTP (FastAPI), presentation (React), and ML (`ml/`) are independent packages.
2. **Honest AI** — ML, deterministic rules, and simulated demo data are documented as different layers. None are implemented in this milestone.
3. **Explainability later, structure now** — fusion and response engines will return structured factors, not opaque scores.
4. **Prototype database, portable URL** — SQLite first; `DATABASE_URL` is the only persistence contract.
5. **No secrets in source** — environment variables via `.env` (gitignored) and `.env.example`.

## Logical layers

| Layer | Location | Responsibility |
| --- | --- | --- |
| Presentation | `frontend/` | Dashboard UX; calls REST APIs |
| API | `backend/app/api/` | Routes, request/response models |
| Application config | `backend/app/core/` | Settings, CORS, future security headers |
| Domain / persistence | `backend/app/` (future `models/`, `services/`) | Storage and orchestration |
| ML | `ml/` | Feature extraction, models, fusion (not wired yet) |
| Data | `data/` | Raw, processed, and simulated artefacts |
| Evaluation | `tests/`, future `docs/` experiment notes | Automated tests and documented metrics |

## Request path (current)

```
Browser (Vite :5173)
    → GET /api/health   (Vite proxy)
        → FastAPI ( :8000 )
            → health route
            → JSON status payload
```

No authentication, no database writes, no ML inference.

## Request path (planned)

```
Dashboard
    → REST: ingest or query signals
        → API services (no ML inside route functions)
            → ml/ feature + model modules (when they exist)
            → deterministic rule modules (labelled as rules)
            → fusion + explanation + response
            → SQLite (later PostgreSQL)
        → JSON: risk, factors, recommended action
```

## Backend package map

```
backend/app/
  main.py              ASGI app factory
  api/routes/health.py Health check
  core/config.py       Environment-backed settings
```

Routers are mounted under `/api`. New modules get their own route files and must not import model training code into the route module beyond a thin service call.

## Frontend package map

```
frontend/src/
  App.jsx              Landing / command-shell
  api/health.js        Health client
  styles.css           Dashboard aesthetic
```

## Database

`DATABASE_URL` defaults to SQLite under `data/`. No ORM models are registered yet. When persistence is added, use SQLAlchemy (or equivalent) with the same URL so PostgreSQL is a driver change, not a rewrite.

## Why this split is jury-explainable

In five minutes we can point at: **signals in**, **separate analysers**, **fusion with a written methodology**, **explanations**, **defensive recommendations**, **dashboard**. This milestone proves the skeleton and that the UI can reach the API.
