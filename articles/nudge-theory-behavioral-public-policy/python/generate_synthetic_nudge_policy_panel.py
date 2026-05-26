"""Generate synthetic nudge policy panel and experiment data.

The dataset is synthetic and designed for economist-facing nudge theory,
public-policy evaluation, welfare, and behavioral-economics workflows.
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

rng = np.random.default_rng(7070)

N_AGENTS = 8000
PERIODS = 4

regimes = np.array([
    "information_only",
    "reminder_plus_norm",
    "default_plus_reminder",
])
assigned = rng.choice(regimes, size=N_AGENTS, replace=True, p=[0.34, 0.33, 0.33])

agents = pd.DataFrame({
    "agent_id": np.arange(1, N_AGENTS + 1),
    "regime": assigned,
    "default_sensitivity": np.clip(rng.normal(0.55, 0.18, N_AGENTS), 0, 1),
    "reminder_sensitivity": np.clip(rng.normal(0.50, 0.17, N_AGENTS), 0, 1),
    "norm_sensitivity": np.clip(rng.normal(0.48, 0.19, N_AGENTS), 0, 1),
    "friction_sensitivity": np.clip(rng.normal(0.60, 0.16, N_AGENTS), 0, 1),
    "present_bias": np.clip(rng.beta(2, 5, N_AGENTS), 0.05, 0.99),
    "administrative_burden_sensitivity": np.clip(rng.normal(0.58, 0.17, N_AGENTS), 0, 1),
    "trust": np.clip(rng.normal(0.55, 0.20, N_AGENTS), 0, 1),
})

regime_params = {
    "information_only": {
        "default_on": 0,
        "reminder_strength": 0.10,
        "norm_signal": 0.10,
        "friction": 0.22,
        "administrative_burden": 0.25,
    },
    "reminder_plus_norm": {
        "default_on": 0,
        "reminder_strength": 0.70,
        "norm_signal": 0.70,
        "friction": 0.12,
        "administrative_burden": 0.15,
    },
    "default_plus_reminder": {
        "default_on": 1,
        "reminder_strength": 0.70,
        "norm_signal": 0.60,
        "friction": 0.10,
        "administrative_burden": 0.10,
    },
}

rows = []

for _, row in agents.iterrows():
    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0
        regime = row["regime"] if post else "information_only"
        params = regime_params[regime]

        default_on = params["default_on"]
        reminder_strength = params["reminder_strength"]
        norm_signal = params["norm_signal"]
        friction = params["friction"]
        administrative_burden = params["administrative_burden"]

        utility = (
            0.8 * row["default_sensitivity"] * default_on
            + 0.7 * row["reminder_sensitivity"] * reminder_strength
            + 0.8 * row["norm_sensitivity"] * norm_signal
            + 0.4 * row["trust"]
            - 1.1 * row["friction_sensitivity"] * friction
            - 0.5 * row["present_bias"] * friction
            - 0.9 * row["administrative_burden_sensitivity"] * administrative_burden
        )

        uptake_prob = 1 / (1 + np.exp(-utility))
        adopted = rng.binomial(1, uptake_prob)

        user_benefit = 0.50 * adopted
        social_benefit = 0.40 * adopted
        friction_cost = friction * row["friction_sensitivity"]
        admin_cost = administrative_burden * row["administrative_burden_sensitivity"]
        implementation_cost = 0.04 + 0.03 * reminder_strength + 0.02 * norm_signal

        total_welfare = (
            utility
            + user_benefit
            + social_benefit
            - friction_cost
            - admin_cost
            - implementation_cost
        )

        rows.append({
            "agent_id": int(row["agent_id"]),
            "period": period,
            "post": post,
            "regime": regime,
            "reminder_norm_treat": int(regime == "reminder_plus_norm"),
            "default_reminder_treat": int(regime == "default_plus_reminder"),
            "default_sensitivity": row["default_sensitivity"],
            "reminder_sensitivity": row["reminder_sensitivity"],
            "norm_sensitivity": row["norm_sensitivity"],
            "friction_sensitivity": row["friction_sensitivity"],
            "present_bias": row["present_bias"],
            "administrative_burden_sensitivity": row["administrative_burden_sensitivity"],
            "trust": row["trust"],
            "default_on": default_on,
            "reminder_strength": reminder_strength,
            "norm_signal": norm_signal,
            "friction": friction,
            "administrative_burden": administrative_burden,
            "utility": utility,
            "uptake_prob": uptake_prob,
            "adopted": adopted,
            "user_benefit": user_benefit,
            "social_benefit": social_benefit,
            "friction_cost": friction_cost,
            "admin_cost": admin_cost,
            "implementation_cost": implementation_cost,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("agent_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_nudge_policy_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_nudge_policy_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_nudge_policy_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_nudge_policy_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_nudge_policy_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_nudge_policy_experiment.csv'}")
