# Machine learning package

This directory will hold **actual** model code (training, inference, features).

Do not put FastAPI routes here. Do not add scikit-learn until a real experiment exists.

Planned subpackages:

| Package | Future role |
| --- | --- |
| `phishing/` | Email/phishing signal features and models |
| `url_risk/` | URL / host risk features and models |
| `behaviour/` | Behaviour anomaly features and models |
| `identity/` | Login / identity context features and models |
| `fusion/` | Multi-signal correlation (ML and/or documented rules) |
| `explainability/` | Factor extraction for the dashboard |
| `response/` | Maps fused risk to **defensive** recommendations |

See `docs/AI_INTEGRITY.md`.
