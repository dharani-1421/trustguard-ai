# AI / ML integrity

TrustGuard AI must remain honest under jury questions.

## Three categories (keep them separate)

1. **Actual ML** — A trained or fitted model, or a documented unsupervised method, living under `ml/`, evaluated with a repeatable experiment. Not present in the foundation milestone.
2. **Deterministic security rules** — Thresholds, blocklists, heuristic scores. Must be labelled as rules, never as “the ML model”.
3. **Simulated demo data** — Synthetic events for the hackathon walkthrough. Must be labelled as simulated. No invented “real world” telemetry.

## Metrics policy

Do **not** display or document accuracy, precision, recall, F1, confidence, or detection rate unless:

- the number is computed from a documented dataset and protocol, and
- the experiment is written up (dataset source, split, code path).

Until then, the UI must not show placeholder percentages that look like model performance.

## Foundation milestone

- No scikit-learn models
- No NLP pipelines
- No fake `/predict` responses
- Health check only
