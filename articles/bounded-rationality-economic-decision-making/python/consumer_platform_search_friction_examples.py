from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(26263)
n = 3500

users = pd.DataFrame({
    "user_id": np.arange(1, n + 1),
    "search_skill": rng.uniform(0.10, 1.00, n),
    "time_available": rng.uniform(0.10, 1.00, n),
    "price_sensitivity": rng.uniform(0.10, 1.00, n),
    "digital_access": rng.uniform(0.10, 1.00, n),
    "trust_platform": rng.uniform(0.10, 1.00, n),
    "status_quo_attachment": rng.uniform(0.00, 1.00, n),
})

platform_designs = {
    "transparent_comparison": {"friction": 0.20, "hidden_fee": 0.05, "default_bias": 0.10, "exit_friction": 0.10},
    "standard_marketplace": {"friction": 0.45, "hidden_fee": 0.20, "default_bias": 0.35, "exit_friction": 0.35},
    "dark_pattern_design": {"friction": 0.75, "hidden_fee": 0.45, "default_bias": 0.65, "exit_friction": 0.75},
}

rows = []
for design, p in platform_designs.items():
    for _, user in users.iterrows():
        search_burden = (
            p["friction"]
            + 0.45 * (1 - user["search_skill"])
            + 0.25 * (1 - user["time_available"])
            + 0.20 * (1 - user["digital_access"])
        )

        hidden_total_cost = 50 + 35 * p["hidden_fee"] + rng.normal(0, 5)
        plan_quality = (
            0.65
            + 0.25 * user["search_skill"]
            - 0.35 * search_burden
            - 0.15 * p["default_bias"]
            + rng.normal(0, 0.08)
        )
        plan_quality = min(1, max(0, plan_quality))

        switching_score = (
            -0.25
            + 0.75 * user["price_sensitivity"]
            + 0.55 * user["search_skill"]
            - 1.00 * p["exit_friction"]
            - 0.70 * user["status_quo_attachment"]
            - 0.55 * search_burden
            + rng.normal(0, 0.30)
        )
        switching_probability = 1 / (1 + np.exp(-switching_score))
        switched = rng.binomial(1, switching_probability)

        rows.append({
            "design": design,
            "user_id": user["user_id"],
            "search_skill": user["search_skill"],
            "time_available": user["time_available"],
            "price_sensitivity": user["price_sensitivity"],
            "digital_access": user["digital_access"],
            "trust_platform": user["trust_platform"],
            "status_quo_attachment": user["status_quo_attachment"],
            "search_burden": search_burden,
            "hidden_total_cost": hidden_total_cost,
            "plan_quality": plan_quality,
            "switching_probability": switching_probability,
            "switched": switched,
        })

df = pd.DataFrame(rows)
summary = df.groupby("design").agg(
    users=("user_id", "count"),
    switching_rate=("switched", "mean"),
    mean_search_burden=("search_burden", "mean"),
    mean_hidden_total_cost=("hidden_total_cost", "mean"),
    mean_plan_quality=("plan_quality", "mean"),
).reset_index()

df["search_skill_quartile"] = pd.qcut(df["search_skill"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
heterogeneity = df.groupby(["design", "search_skill_quartile"], observed=False).agg(
    switching_rate=("switched", "mean"),
    mean_search_burden=("search_burden", "mean"),
    mean_plan_quality=("plan_quality", "mean"),
    users=("user_id", "count"),
).reset_index()

df.to_csv(TABLES / "consumer_platform_search_friction_examples.csv", index=False)
summary.to_csv(TABLES / "consumer_platform_search_friction_summary.csv", index=False)
heterogeneity.to_csv(TABLES / "consumer_platform_search_skill_heterogeneity.csv", index=False)

print(summary)
print(heterogeneity.head())
