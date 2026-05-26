"""Generate synthetic regulatory policy panel and experiment data.

The dataset is synthetic and designed for economist-facing regulatory policy,
welfare, public-economics, and behavioral-economics workflows.
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

rng = np.random.default_rng(5050)

N_AGENTS = 7500
PERIODS = 4

regimes = np.array([
    "sanction_heavy_deterrence",
    "simplification_plus_trust",
    "integrated_behavioral_regulation",
])
assigned = rng.choice(regimes, size=N_AGENTS, replace=True, p=[0.34, 0.33, 0.33])

agents = pd.DataFrame({
    "agent_id": np.arange(1, N_AGENTS + 1),
    "regime": assigned,
    "trust": np.clip(rng.normal(0.55, 0.20, N_AGENTS), 0, 1),
    "norm_sensitivity": np.clip(rng.normal(0.48, 0.19, N_AGENTS), 0, 1),
    "burden_sensitivity": np.clip(rng.normal(0.60, 0.16, N_AGENTS), 0, 1),
    "loss_aversion": np.clip(rng.normal(2.00, 0.40, N_AGENTS), 1, 4),
    "private_gain_noncompliance": np.clip(rng.normal(0.30, 0.12, N_AGENTS), 0, 1),
    "compliance_capacity": np.clip(rng.normal(0.62, 0.20, N_AGENTS), 0, 1),
})

regime_params = {
    "sanction_heavy_deterrence": {
        "admin_burden": 0.28,
        "trust_signal": 0.20,
        "norm_signal": 0.20,
        "default_assistance": 0,
        "sanction_strength": 0.85,
    },
    "simplification_plus_trust": {
        "admin_burden": 0.08,
        "trust_signal": 0.80,
        "norm_signal": 0.45,
        "default_assistance": 1,
        "sanction_strength": 0.35,
    },
    "integrated_behavioral_regulation": {
        "admin_burden": 0.10,
        "trust_signal": 0.75,
        "norm_signal": 0.65,
        "default_assistance": 1,
        "sanction_strength": 0.55,
    },
}

panel_rows = []

for _, row in agents.iterrows():
    for period in range(1, PERIODS + 1):
        post = 1 if period >= 3 else 0
        params = regime_params[row["regime"]] if post else regime_params["sanction_heavy_deterrence"]

        admin_burden = params["admin_burden"]
        trust_signal = params["trust_signal"]
        norm_signal = params["norm_signal"]
        default_assistance = params["default_assistance"]
        sanction_strength = params["sanction_strength"]

        utility_compliance = (
            0.7 * row["trust"] * trust_signal
            + 0.8 * row["norm_sensitivity"] * norm_signal
            + 0.6 * default_assistance
            + 0.4 * row["compliance_capacity"]
            - 1.1 * row["burden_sensitivity"] * admin_burden
            - 0.3 * row["loss_aversion"] * admin_burden
        )

        utility_noncompliance = row["private_gain_noncompliance"] - sanction_strength
        net_utility = utility_compliance - utility_noncompliance

        compliance_prob = 1 / (1 + np.exp(-net_utility))
        complied = rng.binomial(1, compliance_prob)

        social_benefit = 0.90 * complied
        compliance_cost = admin_burden * row["burden_sensitivity"]
        enforcement_cost = 0.20 * sanction_strength
        administrative_cost = 0.10 + 0.25 * admin_burden

        total_welfare = (
            utility_compliance
            + social_benefit
            - compliance_cost
            - enforcement_cost
            - administrative_cost
        )

        panel_rows.append({
            "agent_id": int(row["agent_id"]),
            "period": period,
            "post": post,
            "regime": row["regime"],
            "simplification_treat": int(row["regime"] == "simplification_plus_trust"),
            "integrated_treat": int(row["regime"] == "integrated_behavioral_regulation"),
            "trust": row["trust"],
            "norm_sensitivity": row["norm_sensitivity"],
            "burden_sensitivity": row["burden_sensitivity"],
            "loss_aversion": row["loss_aversion"],
            "private_gain_noncompliance": row["private_gain_noncompliance"],
            "compliance_capacity": row["compliance_capacity"],
            "admin_burden": admin_burden,
            "trust_signal": trust_signal,
            "norm_signal": norm_signal,
            "default_assistance": default_assistance,
            "sanction_strength": sanction_strength,
            "utility_compliance": utility_compliance,
            "utility_noncompliance": utility_noncompliance,
            "compliance_prob": compliance_prob,
            "complied": complied,
            "social_benefit": social_benefit,
            "compliance_cost": compliance_cost,
            "enforcement_cost": enforcement_cost,
            "administrative_cost": administrative_cost,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(panel_rows)
experiment = panel.loc[panel["post"] == 1].groupby("agent_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_regulatory_policy_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_regulatory_policy_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_regulatory_policy_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_regulatory_policy_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows to {TABLES / 'synthetic_regulatory_policy_panel.csv'}")
print(f"Wrote {len(experiment):,} experiment rows to {TABLES / 'synthetic_regulatory_policy_experiment.csv'}")
