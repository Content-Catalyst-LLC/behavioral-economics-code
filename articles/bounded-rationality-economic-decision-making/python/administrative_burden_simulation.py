from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(26261)
n = 4000

agents = pd.DataFrame({
    "person_id": np.arange(1, n + 1),
    "eligible": rng.binomial(1, 0.72, n),
    "digital_access": rng.uniform(0.10, 1.00, n),
    "administrative_capacity": rng.uniform(0.10, 1.00, n),
    "institutional_trust": rng.uniform(0.15, 1.00, n),
    "time_scarcity": rng.uniform(0.00, 0.85, n),
    "stress": rng.uniform(0.00, 0.85, n),
    "language_access": rng.uniform(0.25, 1.00, n),
    "income_security": rng.uniform(0.05, 1.00, n),
})

burden_regimes = {
    "high_burden": {"steps": 9, "documentation": 0.85, "stigma": 0.45, "support": 0.15},
    "moderate_burden": {"steps": 5, "documentation": 0.55, "stigma": 0.30, "support": 0.45},
    "simplified": {"steps": 2, "documentation": 0.25, "stigma": 0.10, "support": 0.80},
}

rows = []
for regime, params in burden_regimes.items():
    for _, row in agents.iterrows():
        learning_cost = (
            0.08 * params["steps"]
            + 0.45 * (1 - row["digital_access"])
            + 0.30 * (1 - row["language_access"])
            - 0.20 * params["support"]
        )
        compliance_cost = (
            0.06 * params["steps"]
            + 0.55 * params["documentation"]
            + 0.35 * row["time_scarcity"]
            + 0.25 * (1 - row["administrative_capacity"])
            - 0.25 * params["support"]
        )
        psychological_cost = (
            params["stigma"]
            + 0.35 * row["stress"]
            + 0.25 * (1 - row["institutional_trust"])
            + 0.10 * (1 - row["income_security"])
        )

        total_burden = learning_cost + compliance_cost + psychological_cost

        completion_score = (
            2.0
            + 1.20 * row["eligible"]
            + 0.85 * row["administrative_capacity"]
            + 0.55 * row["digital_access"]
            + 0.55 * row["institutional_trust"]
            - 1.35 * total_burden
            + rng.normal(0, 0.35)
        )
        completion_probability = 1 / (1 + np.exp(-completion_score))
        completed_application = rng.binomial(1, completion_probability)

        takeup_score = (
            -0.30
            + 1.80 * row["eligible"]
            + 1.25 * completed_application
            - 0.55 * total_burden
            + 0.35 * row["institutional_trust"]
            + rng.normal(0, 0.25)
        )
        takeup_probability = 1 / (1 + np.exp(-takeup_score))
        takeup = rng.binomial(1, takeup_probability)

        rows.append({
            "regime": regime,
            "person_id": row["person_id"],
            "eligible": row["eligible"],
            "digital_access": row["digital_access"],
            "administrative_capacity": row["administrative_capacity"],
            "institutional_trust": row["institutional_trust"],
            "time_scarcity": row["time_scarcity"],
            "stress": row["stress"],
            "language_access": row["language_access"],
            "income_security": row["income_security"],
            "learning_cost": learning_cost,
            "compliance_cost": compliance_cost,
            "psychological_cost": psychological_cost,
            "total_burden": total_burden,
            "completion_probability": completion_probability,
            "completed_application": completed_application,
            "takeup_probability": takeup_probability,
            "takeup": takeup,
        })

df = pd.DataFrame(rows)
summary = df.groupby("regime").agg(
    people=("person_id", "count"),
    eligible_share=("eligible", "mean"),
    completion_rate=("completed_application", "mean"),
    takeup_rate=("takeup", "mean"),
    mean_learning_cost=("learning_cost", "mean"),
    mean_compliance_cost=("compliance_cost", "mean"),
    mean_psychological_cost=("psychological_cost", "mean"),
    mean_total_burden=("total_burden", "mean"),
).reset_index()

df["admin_capacity_quartile"] = pd.qcut(df["administrative_capacity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
heterogeneity = df.groupby(["regime", "admin_capacity_quartile"], observed=False).agg(
    completion_rate=("completed_application", "mean"),
    takeup_rate=("takeup", "mean"),
    mean_total_burden=("total_burden", "mean"),
    people=("person_id", "count"),
).reset_index()

df.to_csv(TABLES / "administrative_burden_simulation.csv", index=False)
summary.to_csv(TABLES / "administrative_burden_summary.csv", index=False)
heterogeneity.to_csv(TABLES / "administrative_burden_capacity_heterogeneity.csv", index=False)

print(summary)
print(heterogeneity.head())
