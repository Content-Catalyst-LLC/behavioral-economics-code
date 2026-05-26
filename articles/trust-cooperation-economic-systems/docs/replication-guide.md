# Replication Guide

Recommended requirements:

- Python 3.10+
- R 4.2+
- Stata 17+
- SQLite
- Julia 1.9+

Python dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python3 python/generate_synthetic_trust_cooperation_panel.py
python3 python/causal_trust_cooperation_evaluation.py
python3 python/trust_cooperation_welfare_analysis.py
python3 python/repeated_exchange_simulation.py
```
