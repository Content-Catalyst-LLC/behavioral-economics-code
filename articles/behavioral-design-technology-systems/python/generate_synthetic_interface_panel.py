"""Generate synthetic panel and experiment data for behavioral design evaluation.

The dataset is synthetic and designed for economist-facing teaching and
policy-evaluation workflows.
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

rng = np.random.default_rng(2026)

N_USERS = 6000
PERIODS = 4

regimes = np.array([
    "user_supportive_design",
    "engagement_maximizing_design",
    "friction_heavy_lock_in",
])

assigned = rng.choice(regimes, size=N_USERS, replace=True, p=[0.34, 0.33, 0.33])

users = pd.DataFrame({
    "user_id": np.arange(1, N_USERS + 1),
    "regime": assigned,
    "baseline_value": rng.normal(0.45, 0.18, N_USERS),
    "cognitive_overload": np.clip(rng.normal(0.42, 0.15, N_USERS), 0, 1),
    "privacy_sensitivity": np.clip(rng.normal(0.55, 0.20, N_USERS), 0, 1),
    "autonomy_preference": np.clip(rng.normal(0.58, 0.18, N_USERS), 0, 1),
    "digital_literacy": np.clip(rng.normal(0.62, 0.20, N_USERS), 0, 1),
})

regime_params = {
    "user_supportive_design": {
        "salience": 0.55,
        "default_on": 0,
        "entry_friction": 0.08,
        "exit_friction": 0.08,
        "reward_intensity": 0.35,
        "data_extraction_intensity": 0.10,
    },
    "engagement_maximizing_design": {
        "salience": 0.85,
        "default_on": 1,
        "entry_friction": 0.03,
        "exit_friction": 0.22,
        "reward_intensity": 0.80,
        "data_extraction_intensity": 0.45,
    },
    "friction_heavy_lock_in": {
        "salience": 0.75,
        "default_on": 1,
        "entry_friction": 0.02,
        "exit_friction": 0.60,
        "reward_intensity": 0.55,
        "data_extraction_intensity": 0.60,
    },
}

panel_rows = []

for _, row in users.iterrows():
    params = regime_params[row["regime"]]

    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0

        salience = params["salience"] if post else 0.45
        default_on = params["default_on"] if post else 0
        entry_friction = params["entry_friction"] if post else 0.10
        exit_friction = params["exit_friction"] if post else 0.10
        reward_intensity = params["reward_intensity"] if post else 0.30
        data_extraction_intensity = params["data_extraction_intensity"] if post else 0.10

        friction_asymmetry = exit_friction - entry_friction

        join_score = (
            row["baseline_value"]
            + 0.55 * salience
            + 0.45 * default_on
            - 0.70 * entry_friction
            + 0.35 * reward_intensity
            - 0.35 * row["cognitive_overload"]
            + 0.20 * row["digital_literacy"]
        )

        join_prob = 1 / (1 + np.exp(-join_score))
        joined = rng.binomial(1, join_prob)

        retain_score = (
            0.40 * row["baseline_value"]
            + 0.60 * reward_intensity
            + 0.45 * default_on
            + 0.85 * exit_friction
            - 0.30 * row["cognitive_overload"]
            + 0.15 * row["digital_literacy"]
        )

        retention_prob = 1 / (1 + np.exp(-retain_score))
        retained = rng.binomial(1, retention_prob) if joined else 0

        consent_score = (
            0.25 * row["baseline_value"]
            + 0.50 * default_on
            + 0.35 * salience
            - 0.60 * row["privacy_sensitivity"]
            - 0.25 * row["cognitive_overload"]
        )

        consent_prob = 1 / (1 + np.exp(-consent_score))
        consented = rng.binomial(1, consent_prob)

        autonomy_cost = max(friction_asymmetry, 0) * row["autonomy_preference"] * 0.7
        privacy_cost = data_extraction_intensity * row["privacy_sensitivity"] * consented
        overload_cost = 0.45 * row["cognitive_overload"]

        user_welfare = (
            joined * (row["baseline_value"] + 0.35 * reward_intensity)
            - autonomy_cost
            - privacy_cost
            - overload_cost
        )

        platform_value = (
            1.2 * joined
            + 1.5 * retained
            + 0.9 * consented * data_extraction_intensity
        )

        panel_rows.append({
            "user_id": int(row["user_id"]),
            "period": period,
            "post": post,
            "regime": row["regime"],
            "engagement_design": int(row["regime"] == "engagement_maximizing_design"),
            "lockin_design": int(row["regime"] == "friction_heavy_lock_in"),
            "baseline_value": row["baseline_value"],
            "cognitive_overload": row["cognitive_overload"],
            "privacy_sensitivity": row["privacy_sensitivity"],
            "autonomy_preference": row["autonomy_preference"],
            "digital_literacy": row["digital_literacy"],
            "salience": salience,
            "default_on": default_on,
            "entry_friction": entry_friction,
            "exit_friction": exit_friction,
            "friction_asymmetry": friction_asymmetry,
            "reward_intensity": reward_intensity,
            "data_extraction_intensity": data_extraction_intensity,
            "joined": joined,
            "retained": retained,
            "consented": consented,
            "user_welfare": user_welfare,
            "platform_value": platform_value,
            "welfare_platform_gap": platform_value - user_welfare,
        })

panel = pd.DataFrame(panel_rows)

experiment = panel.loc[panel["post"] == 1].groupby("user_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_interface_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_interface_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_interface_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_interface_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_interface_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_interface_experiment.csv'}")
