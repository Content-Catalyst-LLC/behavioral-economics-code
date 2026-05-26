"""Generate synthetic platform panel and experiment data.

The dataset is synthetic and designed for economist-facing platform-policy,
welfare, and behavioral-economics workflows.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"

for folder in (RAW, PROCESSED, TABLES):
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(3030)

N_USERS = 6500
PERIODS = 4

regimes = np.array(["neutral_discovery", "engagement_optimized", "socially_amplified_ranking"])
assigned = rng.choice(regimes, size=N_USERS, replace=True, p=[0.34, 0.33, 0.33])

users = pd.DataFrame({
    "user_id": np.arange(1, N_USERS + 1),
    "regime": assigned,
    "baseline_user_value": rng.normal(0.45, 0.18, N_USERS),
    "cognitive_overload": np.clip(rng.normal(0.42, 0.15, N_USERS), 0, 1),
    "privacy_sensitivity": np.clip(rng.normal(0.55, 0.20, N_USERS), 0, 1),
    "digital_literacy": np.clip(rng.normal(0.62, 0.20, N_USERS), 0, 1),
    "social_susceptibility": np.clip(rng.normal(0.46, 0.20, N_USERS), 0, 1),
})

regime_params = {
    "neutral_discovery": {
        "recommendation_intensity": 0.45,
        "salience": 0.45,
        "social_proof": 0.20,
        "friction": 0.18,
        "data_extraction_intensity": 0.10,
        "platform_revenue_weight": 0.40,
    },
    "engagement_optimized": {
        "recommendation_intensity": 0.85,
        "salience": 0.80,
        "social_proof": 0.55,
        "friction": 0.10,
        "data_extraction_intensity": 0.45,
        "platform_revenue_weight": 0.85,
    },
    "socially_amplified_ranking": {
        "recommendation_intensity": 0.70,
        "salience": 0.65,
        "social_proof": 0.90,
        "friction": 0.12,
        "data_extraction_intensity": 0.35,
        "platform_revenue_weight": 0.70,
    },
}

rows = []

for _, row in users.iterrows():
    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0

        params = regime_params[row["regime"]] if post else regime_params["neutral_discovery"]

        recommendation_intensity = params["recommendation_intensity"]
        salience = params["salience"]
        social_proof = params["social_proof"]
        friction = params["friction"]
        data_extraction_intensity = params["data_extraction_intensity"]
        platform_revenue_weight = params["platform_revenue_weight"]

        click_score = (
            row["baseline_user_value"]
            + 0.50 * recommendation_intensity
            + 0.45 * salience
            + 0.40 * row["social_susceptibility"] * social_proof
            - 0.55 * friction
            - 0.25 * row["cognitive_overload"]
            + 0.15 * row["digital_literacy"]
        )

        click_prob = 1 / (1 + np.exp(-click_score))
        clicked = rng.binomial(1, click_prob)

        retain_score = (
            0.35 * row["baseline_user_value"]
            + 0.70 * recommendation_intensity
            + 0.55 * salience
            + 0.30 * social_proof
            - 0.20 * row["cognitive_overload"]
        )
        retained = rng.binomial(1, 1 / (1 + np.exp(-retain_score))) if clicked else 0

        consent_score = (
            0.25 * row["baseline_user_value"]
            + 0.35 * salience
            + 0.25 * recommendation_intensity
            - 0.65 * row["privacy_sensitivity"]
            - 0.20 * row["cognitive_overload"]
        )
        consented = rng.binomial(1, 1 / (1 + np.exp(-consent_score)))

        exposure_quality = (
            row["baseline_user_value"]
            + rng.normal(0, 0.08)
            - 0.10 * max(recommendation_intensity - 0.70, 0)
            - 0.08 * max(social_proof - 0.70, 0)
        )

        user_welfare = (
            clicked * exposure_quality
            - 0.30 * row["cognitive_overload"]
            - 0.45 * row["privacy_sensitivity"] * data_extraction_intensity * consented
            - 0.15 * friction
        )

        platform_value = (
            1.1 * clicked
            + 1.3 * retained
            + platform_revenue_weight
            + 0.7 * data_extraction_intensity * consented
        )

        rows.append({
            "user_id": int(row["user_id"]),
            "period": period,
            "post": post,
            "regime": row["regime"],
            "engagement_optimized": int(row["regime"] == "engagement_optimized"),
            "socially_amplified": int(row["regime"] == "socially_amplified_ranking"),
            "baseline_user_value": row["baseline_user_value"],
            "cognitive_overload": row["cognitive_overload"],
            "privacy_sensitivity": row["privacy_sensitivity"],
            "digital_literacy": row["digital_literacy"],
            "social_susceptibility": row["social_susceptibility"],
            "recommendation_intensity": recommendation_intensity,
            "salience": salience,
            "social_proof": social_proof,
            "friction": friction,
            "data_extraction_intensity": data_extraction_intensity,
            "clicked": clicked,
            "retained": retained,
            "consented": consented,
            "exposure_quality": exposure_quality,
            "user_welfare": user_welfare,
            "platform_value": platform_value,
            "welfare_platform_gap": platform_value - user_welfare,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("user_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_platform_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_platform_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_platform_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_platform_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_platform_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_platform_experiment.csv'}")
