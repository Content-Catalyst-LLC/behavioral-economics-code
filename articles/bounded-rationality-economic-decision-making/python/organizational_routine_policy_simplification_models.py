from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(26262)

# Organizational routine simulation.
n_orgs = 1500
periods = 8

orgs = pd.DataFrame({
    "org_id": np.arange(1, n_orgs + 1),
    "routine_strength": rng.uniform(0.10, 1.00, n_orgs),
    "learning_capacity": rng.uniform(0.10, 1.00, n_orgs),
    "frontline_feedback": rng.uniform(0.10, 1.00, n_orgs),
    "metric_quality": rng.uniform(0.10, 1.00, n_orgs),
})

org_rows = []
for _, org in orgs.iterrows():
    for t in range(1, periods + 1):
        environment_change = rng.binomial(1, 0.28 if t >= 4 else 0.10)
        routine_benefit = 0.45 * org["routine_strength"] * (1 - environment_change)
        routine_rigidity_penalty = 0.55 * org["routine_strength"] * environment_change * (1 - org["learning_capacity"])
        feedback_benefit = 0.40 * org["frontline_feedback"] * environment_change
        metric_benefit = 0.25 * org["metric_quality"]

        performance = (
            0.55
            + routine_benefit
            - routine_rigidity_penalty
            + feedback_benefit
            + metric_benefit
            + rng.normal(0, 0.08)
        )
        performance = max(0, min(1, performance))

        org_rows.append({
            "org_id": org["org_id"],
            "period": t,
            "routine_strength": org["routine_strength"],
            "learning_capacity": org["learning_capacity"],
            "frontline_feedback": org["frontline_feedback"],
            "metric_quality": org["metric_quality"],
            "environment_change": environment_change,
            "performance": performance,
        })

org_df = pd.DataFrame(org_rows)
org_summary = org_df.groupby("environment_change").agg(
    observations=("org_id", "count"),
    mean_performance=("performance", "mean"),
    mean_routine_strength=("routine_strength", "mean"),
    mean_learning_capacity=("learning_capacity", "mean"),
    mean_frontline_feedback=("frontline_feedback", "mean"),
).reset_index()

# Policy simplification simulation.
n = 3000
users = pd.DataFrame({
    "user_id": np.arange(1, n + 1),
    "baseline_need": rng.uniform(0.20, 1.00, n),
    "administrative_capacity": rng.uniform(0.10, 1.00, n),
    "digital_access": rng.uniform(0.10, 1.00, n),
    "trust": rng.uniform(0.10, 1.00, n),
    "time_scarcity": rng.uniform(0.00, 0.85, n),
})

simplification_arms = {
    "status_quo": {"steps": 8, "default": 0, "navigator": 0, "prefill": 0},
    "plain_language": {"steps": 6, "default": 0, "navigator": 0, "prefill": 0},
    "prefilled_forms": {"steps": 4, "default": 0, "navigator": 0, "prefill": 1},
    "automatic_enrollment": {"steps": 2, "default": 1, "navigator": 1, "prefill": 1},
}

policy_rows = []
for arm, p in simplification_arms.items():
    for _, user in users.iterrows():
        procedural_burden = (
            0.12 * p["steps"]
            + 0.45 * (1 - user["administrative_capacity"])
            + 0.25 * (1 - user["digital_access"])
            + 0.30 * user["time_scarcity"]
            - 0.25 * p["prefill"]
            - 0.25 * p["navigator"]
        )
        comprehension = min(1, max(0, 0.35 + 0.35 * user["administrative_capacity"] + 0.20 * p["prefill"] + 0.10 * p["navigator"] - 0.05 * p["steps"]))
        takeup_score = (
            -0.20
            + 1.10 * user["baseline_need"]
            + 0.85 * user["trust"]
            + 0.75 * p["default"]
            + 0.35 * p["navigator"]
            - 1.10 * procedural_burden
            + rng.normal(0, 0.30)
        )
        takeup_probability = 1 / (1 + np.exp(-takeup_score))
        takeup = rng.binomial(1, takeup_probability)

        policy_rows.append({
            "arm": arm,
            "user_id": user["user_id"],
            "baseline_need": user["baseline_need"],
            "administrative_capacity": user["administrative_capacity"],
            "digital_access": user["digital_access"],
            "trust": user["trust"],
            "time_scarcity": user["time_scarcity"],
            "procedural_burden": procedural_burden,
            "comprehension": comprehension,
            "takeup_probability": takeup_probability,
            "takeup": takeup,
        })

policy_df = pd.DataFrame(policy_rows)
policy_summary = policy_df.groupby("arm").agg(
    users=("user_id", "count"),
    takeup_rate=("takeup", "mean"),
    mean_procedural_burden=("procedural_burden", "mean"),
    mean_comprehension=("comprehension", "mean"),
    mean_need=("baseline_need", "mean"),
).reset_index()

org_df.to_csv(TABLES / "organizational_routine_simulation.csv", index=False)
org_summary.to_csv(TABLES / "organizational_routine_summary.csv", index=False)
policy_df.to_csv(TABLES / "policy_simplification_simulation.csv", index=False)
policy_summary.to_csv(TABLES / "policy_simplification_summary.csv", index=False)

print(org_summary)
print(policy_summary)
