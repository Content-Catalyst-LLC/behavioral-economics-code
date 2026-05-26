"""Generate synthetic environmental policy panel and experiment data.

The dataset is synthetic and designed for economist-facing environmental policy,
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

rng = np.random.default_rng(4040)

N_HOUSEHOLDS = 7000
PERIODS = 4

regimes = np.array(["price_signal_only", "norm_plus_default", "integrated_policy_design"])
assigned = rng.choice(regimes, size=N_HOUSEHOLDS, replace=True, p=[0.34, 0.33, 0.33])

households = pd.DataFrame({
    "household_id": np.arange(1, N_HOUSEHOLDS + 1),
    "regime": assigned,
    "income": rng.lognormal(np.log(55000), 0.55, N_HOUSEHOLDS),
    "energy_burden": np.clip(rng.normal(0.08, 0.04, N_HOUSEHOLDS), 0.01, 0.30),
    "env_concern": np.clip(rng.normal(0.60, 0.18, N_HOUSEHOLDS), 0, 1),
    "present_bias": np.clip(rng.beta(2, 5, N_HOUSEHOLDS), 0.05, 0.99),
    "norm_sensitivity": np.clip(rng.normal(0.50, 0.20, N_HOUSEHOLDS), 0, 1),
    "friction_sensitivity": np.clip(rng.normal(0.58, 0.17, N_HOUSEHOLDS), 0, 1),
    "loss_aversion": np.clip(rng.normal(2.00, 0.40, N_HOUSEHOLDS), 1, 4),
    "trust": np.clip(rng.normal(0.55, 0.20, N_HOUSEHOLDS), 0, 1),
})

regime_params = {
    "price_signal_only": {
        "subsidy": 0.08,
        "default_green": 0,
        "norm_signal": 0.10,
        "friction": 0.20,
    },
    "norm_plus_default": {
        "subsidy": 0.00,
        "default_green": 1,
        "norm_signal": 0.70,
        "friction": 0.08,
    },
    "integrated_policy_design": {
        "subsidy": 0.06,
        "default_green": 1,
        "norm_signal": 0.70,
        "friction": 0.08,
    },
}

panel_rows = []

for _, row in households.iterrows():
    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0
        params = regime_params[row["regime"]] if post else regime_params["price_signal_only"]

        subsidy = params["subsidy"]
        default_green = params["default_green"]
        norm_signal = params["norm_signal"]
        friction = params["friction"]

        upfront_cost = max(0.18 - subsidy, 0.0)

        utility = (
            0.9 * row["env_concern"]
            + 0.8 * row["norm_sensitivity"] * norm_signal
            + 0.7 * default_green
            + 0.5 * row["trust"]
            - 1.2 * upfront_cost
            - 1.0 * friction * row["friction_sensitivity"]
            - 0.6 * row["present_bias"] * upfront_cost
            - 0.4 * row["loss_aversion"] * friction
            - 0.5 * row["energy_burden"]
        )

        uptake_prob = 1 / (1 + np.exp(-utility))
        adopted = rng.binomial(1, uptake_prob)

        private_benefit = adopted * (0.25 + 0.15 * row["energy_burden"])
        environmental_benefit = adopted * 0.90
        fiscal_cost = adopted * subsidy
        admin_cost = 0.05 + 0.10 * friction
        friction_cost = friction * row["friction_sensitivity"]

        total_welfare = (
            utility
            + private_benefit
            + environmental_benefit
            - fiscal_cost
            - admin_cost
            - 0.20 * friction_cost
        )

        panel_rows.append({
            "household_id": int(row["household_id"]),
            "period": period,
            "post": post,
            "regime": row["regime"],
            "norm_default_treat": int(row["regime"] == "norm_plus_default"),
            "integrated_treat": int(row["regime"] == "integrated_policy_design"),
            "income": row["income"],
            "energy_burden": row["energy_burden"],
            "env_concern": row["env_concern"],
            "present_bias": row["present_bias"],
            "norm_sensitivity": row["norm_sensitivity"],
            "friction_sensitivity": row["friction_sensitivity"],
            "loss_aversion": row["loss_aversion"],
            "trust": row["trust"],
            "subsidy": subsidy,
            "default_green": default_green,
            "norm_signal": norm_signal,
            "friction": friction,
            "upfront_cost": upfront_cost,
            "uptake_prob": uptake_prob,
            "adopted": adopted,
            "private_benefit": private_benefit,
            "environmental_benefit": environmental_benefit,
            "fiscal_cost": fiscal_cost,
            "admin_cost": admin_cost,
            "friction_cost": friction_cost,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(panel_rows)
experiment = panel.loc[panel["post"] == 1].groupby("household_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_environmental_policy_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_environmental_policy_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_environmental_policy_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_environmental_policy_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_environmental_policy_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_environmental_policy_experiment.csv'}")
