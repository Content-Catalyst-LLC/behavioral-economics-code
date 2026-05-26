from __future__ import annotations

from pathlib import Path
import itertools
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(25251)

def prospect_value(x, lam, alpha, beta):
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** alpha, -lam * ((-x_arr) ** beta))

def probability_weight(p, gamma):
    p_arr = np.asarray(p, dtype=float)
    return (p_arr ** gamma) / ((p_arr ** gamma + (1 - p_arr) ** gamma) ** (1 / gamma))

n = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n),
    "alpha_gain": rng.uniform(0.75, 1.0, n),
    "beta_loss": rng.uniform(0.75, 1.0, n),
    "gamma_weight": rng.uniform(0.55, 1.0, n),
})

domains = [
    ("gain_high_probability", "gain", 0.90, 120, 0, 95),
    ("gain_low_probability", "gain", 0.05, 2500, 0, 80),
    ("loss_high_probability", "loss", 0.90, -120, 0, -95),
    ("loss_low_probability", "loss", 0.05, -2500, 0, -80),
]

rows = []
for scenario, domain, p_event, risky_event, risky_other, sure_outcome in domains:
    for _, row in agents.iterrows():
        lam = row["lambda_loss"]
        alpha = row["alpha_gain"]
        beta = row["beta_loss"]
        gamma = row["gamma_weight"]

        risky_value = (
            probability_weight(p_event, gamma) * prospect_value(risky_event, lam, alpha, beta)
            + probability_weight(1 - p_event, gamma) * prospect_value(risky_other, lam, alpha, beta)
        )
        sure_value = prospect_value(sure_outcome, lam, alpha, beta)

        rows.append({
            "agent_id": row["agent_id"],
            "scenario": scenario,
            "domain": domain,
            "p_event": p_event,
            "risky_event": risky_event,
            "sure_outcome": sure_outcome,
            "risky_value": float(risky_value),
            "sure_value": float(sure_value),
            "choose_risky": int(risky_value > sure_value),
            "lambda_loss": lam,
            "gamma_weight": gamma,
        })

df = pd.DataFrame(rows)

summary = df.groupby(["scenario", "domain"]).agg(
    agents=("agent_id", "count"),
    share_choose_risky=("choose_risky", "mean"),
    mean_risky_value=("risky_value", "mean"),
    mean_sure_value=("sure_value", "mean"),
    mean_lambda=("lambda_loss", "mean"),
    mean_gamma=("gamma_weight", "mean"),
).reset_index()

df.to_csv(TABLES / "fourfold_risk_attitudes_simulation.csv", index=False)
summary.to_csv(TABLES / "fourfold_risk_attitudes_summary.csv", index=False)

print(summary)
