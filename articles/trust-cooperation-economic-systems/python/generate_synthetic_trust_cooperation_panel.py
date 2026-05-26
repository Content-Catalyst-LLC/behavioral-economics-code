from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(8080)
n_agents = 8000
periods = 4

regimes = np.array([
    "low_trust_exchange",
    "reciprocal_market_exchange",
    "institutionally_supported_cooperation",
])

assigned = rng.choice(regimes, size=n_agents, p=[0.34, 0.33, 0.33])

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "regime": assigned,
    "trust_propensity": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
    "reciprocity": np.clip(rng.normal(0.50, 0.20, n_agents), 0, 1),
    "punishment_willingness": np.clip(rng.normal(0.40, 0.18, n_agents), 0, 1),
    "institutional_trust": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "betrayal_sensitivity": np.clip(rng.normal(0.60, 0.16, n_agents), 0, 1),
    "monitoring_cost_sensitivity": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
})

params = {
    "low_trust_exchange": (0.10, 0.15, 0.70, 0.35),
    "reciprocal_market_exchange": (0.45, 0.55, 0.50, 0.20),
    "institutionally_supported_cooperation": (0.80, 0.75, 0.35, 0.10),
}

rows = []
for _, row in agents.iterrows():
    for period in range(1, periods + 1):
        post = int(period >= 3)
        regime = row["regime"] if post else "low_trust_exchange"
        institutional_support, norm_strength, betrayal_cost, monitoring_intensity = params[regime]

        trust_utility = (
            1.8 * row["trust_propensity"]
            + 0.9 * institutional_support
            + 0.7 * norm_strength
            + 0.4 * row["institutional_trust"]
            - 0.8 * row["betrayal_sensitivity"]
            - 0.5
        )
        trust_prob = 1 / (1 + np.exp(-trust_utility))
        trusted = rng.binomial(1, trust_prob)

        reciprocity_utility = 1.8 * row["reciprocity"] + 0.8 * norm_strength + 0.6 * institutional_support - 0.4
        reciprocity_prob = 1 / (1 + np.exp(-reciprocity_utility))
        reciprocated = rng.binomial(1, reciprocity_prob) if trusted else 0

        punishment_utility = 1.7 * row["punishment_willingness"] + 0.5 * institutional_support - 0.7
        punishment_prob = 1 / (1 + np.exp(-punishment_utility))
        betrayed = int(trusted == 1 and reciprocated == 0)
        punished = rng.binomial(1, punishment_prob) if betrayed else 0

        monitoring_cost = monitoring_intensity * row["monitoring_cost_sensitivity"]
        transaction_cost_reduction = 0.30 * institutional_support + 0.25 * norm_strength + 0.20 * trusted
        cooperative_benefit = trusted * 0.70 * reciprocated
        betrayal_loss = trusted * betrayal_cost * (1 - reciprocated)
        punishment_value = 0.20 * punished
        institutional_cost = 0.05 * institutional_support

        total_welfare = (
            cooperative_benefit
            + transaction_cost_reduction
            + punishment_value
            - betrayal_loss
            - monitoring_cost
            - institutional_cost
        )

        rows.append({
            "agent_id": int(row["agent_id"]),
            "period": period,
            "post": post,
            "regime": regime,
            "reciprocal_market_treat": int(regime == "reciprocal_market_exchange"),
            "institutional_support_treat": int(regime == "institutionally_supported_cooperation"),
            "trust_propensity": row["trust_propensity"],
            "reciprocity": row["reciprocity"],
            "punishment_willingness": row["punishment_willingness"],
            "institutional_trust": row["institutional_trust"],
            "betrayal_sensitivity": row["betrayal_sensitivity"],
            "monitoring_cost_sensitivity": row["monitoring_cost_sensitivity"],
            "institutional_support": institutional_support,
            "norm_strength": norm_strength,
            "betrayal_cost": betrayal_cost,
            "monitoring_intensity": monitoring_intensity,
            "trust_prob": trust_prob,
            "trusted": trusted,
            "reciprocity_prob": reciprocity_prob,
            "reciprocated": reciprocated,
            "punishment_prob": punishment_prob,
            "betrayed": betrayed,
            "punished": punished,
            "monitoring_cost": monitoring_cost,
            "transaction_cost_reduction": transaction_cost_reduction,
            "cooperative_benefit": cooperative_benefit,
            "betrayal_loss": betrayal_loss,
            "punishment_value": punishment_value,
            "institutional_cost": institutional_cost,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("agent_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_trust_cooperation_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_trust_cooperation_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_trust_cooperation_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_trust_cooperation_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows.")
print(f"Wrote {len(experiment):,} experiment rows.")
