# Data directory

No datasets are bundled in the foundation milestone.

| Path | Intended use |
| --- | --- |
| `raw/` | Original files with documented provenance |
| `processed/` | Derived features produced by code |
| `simulated/` | Explicitly labelled **simulated** demo events |

Do not invent labelled “real” attack corpora. Simulated files must be described as simulated.

SQLite (when added) may live here as `trustguard.db` (gitignored).
