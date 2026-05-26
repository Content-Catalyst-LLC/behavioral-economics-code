"""Generate synthetic choice architecture panel and experiment data.

The dataset is synthetic and designed for economist-facing choice-architecture,
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

rng = np.random.default_rng(6060)

N_USERS = 8000
PERIODS = 4
N_OPTIONS = 4

regimes = np.array([
    "neutral_presentation",
    "default_heavy_architecture",
    "low_complexity_guided_design",
])
assigned = rng.choice(regimes, size=N_USERS, replace=True, p=[0.34, 0.33, 0.33])

users = pd.DataFrame({
    "user_id": np.arange(1, N_USERS + 1),
    "regime": assigned,
    "default_sensitivity": np.clip(rng.normal(0.55, 0.18, N_USERS), 0, 1),
    "salience_sensitivity": np.clip(rng.normal(0.50, 0.17, N_USERS), 0, 1),
    "framing_sensitivity": np.clip(rng.normal(0.45, 0.16, N_USERS), 0, 1),
    "complexity_sensitivity": np.clip(rng.normal(0.60, 0.16, N_USERS), 0, 1),
    "switching_cost_sensitivity": np.clip(rng.normal(0.52, 0.18, N_USERS), 0, 1),
    "digital_literacy": np.clip(rng.normal(0.62, 0.20, N_USERS), 0, 1),
    "institutional_trust": np.clip(rng.normal(0.55, 0.20, N_USERS), 0, 1),
})

base_values = np.array([0.30, 0.28, 0.26, 0.24])
long_run_values = np.array([0.42, 0.36, 0.32, 0.30])

regime_params = {
    "neutral_presentation": {
        "default_flags": np.array([0, 0, 0, 0]),
        "salience": np.array([0.50, 0.50, 0.50, 0.50]),
        "framing": np.array([0.50, 0.50, 0.50, 0.50]),
        "complexity": np.array([0.20, 0.20, 0.20, 0.20]),
        "switching_cost": np.array([0.05, 0.05, 0.05, 0.05]),
    },
    "default_heavy_architecture": {
        "default_flags": np.array([1, 0, 0, 0]),
        "salience": np.array([0.85, 0.45, 0.40, 0.35]),
        "framing": np.array([0.75, 0.45, 0.45, 0.35]),
        "complexity": np.array([0.12, 0.25, 0.30, 0.35]),
        "switching_cost": np.array([0.02, 0.15, 0.18, 0.20]),
    },
    "low_complexity_guided_design": {
        "default_flags": np.array([0, 0, 0, 0]),
        "salience": np.array([0.65, 0.60, 0.55, 0.50]),
        "framing": np.array([0.65, 0.60, 0.58, 0.55]),
        "complexity": np.array([0.08, 0.10, 0.12, 0.15]),
        "switching_cost": np.array([0.04, 0.05, 0.06, 0.07]),
    },
}

rows = []

for _, user in users.iterrows():
    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0
        regime = user["regime"] if post else "neutral_presentation"
        params = regime_params[regime]

        utility = (
            base_values
            + user["default_sensitivity"] * params["default_flags"]
            + user["salience_sensitivity"] * params["salience"]
            + user["framing_sensitivity"] * params["framing"]
            - user["complexity_sensitivity"] * params["complexity"]
            - user["switching_cost_sensitivity"] * params["switching_cost"]
            + 0.05 * user["institutional_trust"] * params["default_flags"]
            + 0.03 * user["digital_literacy"] * (1 - params["complexity"])
        )

        probabilities = np.exp(utility - utility.max())
        probabilities = probabilities / probabilities.sum()

        chosen_index = int(rng.choice(N_OPTIONS, p=probabilities))
        chosen_option = chosen_index + 1

        cognitive_cost = float(user["complexity_sensitivity"] * params["complexity"][chosen_index])
        switching_cost = float(user["switching_cost_sensitivity"] * params["switching_cost"][chosen_index])

        realized_welfare = (
            long_run_values[chosen_index]
            - cognitive_cost
            - switching_cost
            + 0.03 * user["digital_literacy"]
        )

        rows.append({
            "user_id": int(user["user_id"]),
            "period": period,
            "post": post,
            "regime": regime,
            "default_heavy_treat": int(regime == "default_heavy_architecture"),
            "guided_design_treat": int(regime == "low_complexity_guided_design"),
            "default_sensitivity": user["default_sensitivity"],
            "salience_sensitivity": user["salience_sensitivity"],
            "framing_sensitivity": user["framing_sensitivity"],
            "complexity_sensitivity": user["complexity_sensitivity"],
            "switching_cost_sensitivity": user["switching_cost_sensitivity"],
            "digital_literacy": user["digital_literacy"],
            "institutional_trust": user["institutional_trust"],
            "chosen_option": chosen_option,
            "chosen_utility": float(utility[chosen_index]),
            "realized_welfare": float(realized_welfare),
            "selected_default": int(params["default_flags"][chosen_index] == 1),
            "selected_high_value_option": int(chosen_index == 0),
            "cognitive_cost": cognitive_cost,
            "switching_cost": switching_cost,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("user_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_choice_architecture_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_choice_architecture_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_choice_architecture_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_choice_architecture_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_choice_architecture_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_choice_architecture_experiment.csv'}")
