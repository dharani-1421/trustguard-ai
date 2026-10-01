# TrustGuard AI

**Adaptive AI for Cyber Threat Detection & Digital Trust**

Cyber AI Hackathon 2026 — University of Derby, UK  
Theme: Cybersecurity & Digital Trust

TrustGuard AI is a **defensive** research prototype. It will combine multiple digital security signals (phishing/email indicators, URL risk, login/identity context, and user behaviour) into an **explainable contextual risk assessment** and a recommended security response.

This repository currently contains the **project foundation only**. Detection modules, risk fusion, and demo simulation are **not implemented yet**.

---

## What this prototype is (and is not)

| This project **will** | This project **will not** |
| --- | --- |
| Use simulated / documented demo data | Use real credentials, personal data, or live attack infrastructure |
| Separate ML, deterministic rules, and demo fixtures | Call rule-based logic “machine learning” |
| Report metrics only from documented experiments | Invent accuracy, F1, or detection rates |
| Recommend defensive responses | Implement malware, credential theft, exploits, or attack automation |

---

## Repository layout

```
frontend/     React + Vite dashboard shell
backend/      FastAPI REST API
ml/           AI/ML packages (placeholders — no models yet)
data/         Data directories (empty by design; no invented datasets)
tests/        Automated tests
docs/         Architecture and integrity notes
```

API routes stay in `backend/`. ML code lives in `ml/` so models are not mixed into HTTP handlers.

---

## Architecture (target pipeline)

```
Digital Signals
    → Data collection
    → Preprocessing / feature extraction
    → AI / ML analysis          (ml/ — not implemented in this milestone)
    → Multi-signal risk correlation
    → Digital trust / risk score
    → Explainable risk factors
    → Response recommendation
    → Cybersecurity dashboard   (frontend/)
```

**Planned modules** (folders exist; logic is deferred):

- Phishing intelligence  
- URL risk analysis  
- User behaviour anomaly detection  
- Identity / login risk  
- AI risk fusion engine  
- Explainable risk analysis  
- Response recommendation engine  
- Cybersecurity command dashboard  
- Attack simulation / demo mode (safe simulated data only)  
- Evaluation and testing  

**Risk score methodology:** not defined yet. See `docs/RISK_METHODOLOGY.md`. Do not treat any UI number as a validated detection metric.

---

## Prerequisites

- Python 3.9+
- Node.js 18+ (npm)
- Git

---

## Quick start

### 1. Backend

```powershell
cd C:\TRUSTGUARD-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Health check: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Frontend

In a second terminal:

```powershell
cd C:\TRUSTGUARD-AI\frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The landing page calls `/api/health` (proxied to the backend) and reports whether the API is reachable.

### 3. Tests

From the repository root, with the virtualenv activated and backend dependencies installed:

```powershell
pip install -r backend\requirements.txt
pytest
```

Frontend production build (optional check):

```powershell
cd frontend
npm run build
```

---

## Configuration

Copy `.env.example` to `.env`. Secrets must never be hard-coded. The prototype uses SQLite via `DATABASE_URL`; the same setting can later point at PostgreSQL.

Frontend: `VITE_API_BASE_URL` is optional. Local Vite development proxies `/api` to `http://127.0.0.1:8000`.

---

## Technology choices (this milestone)

| Layer | Choice | Notes |
| --- | --- | --- |
| Frontend | React + Vite | Dashboard shell + health connectivity |
| Styling | Plain CSS | Cybersecurity aesthetic; no UI framework required yet |
| Backend | FastAPI | REST; health endpoint only |
| Database | SQLite (planned) | URL configured; no schema/migrations yet |
| Charts | *Deferred* | A React chart library will be added when the dashboard has real series to plot |
| ML | *Deferred* | scikit-learn / NLP will be added when a real training or inference path exists |

---

## AI / ML integrity

See `docs/AI_INTEGRITY.md`. Until an experiment is documented, this codebase contains **no trained models**, **no claimed accuracy**, and **no fake inference APIs**.

---

## Security posture

Defensive cybersecurity research / hackathon demo. Attack-related UI later must use **safe simulated data** only.
