from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(10010)
n_agents = 9000
periods = 4

regimes = np.array([
    "fair_cooperative_regime",
    "unequal_but_cooperative_regime",
    "unequal_noncooperative_regime",
    "exploitative_low_process_fairness_regime",
])

assigned = rng.choice(regimes, size=n_agents, p=[0.28, 0.26, 0.24, 0.22])

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "assigned_regime": assigned,
    "fairness_sensitivity": np.clip(rng.normal(1.2, 0.4, n_agents), 0, 3),
    "reciprocity_sensitivity": np.clip(rng.normal(1.0, 0.35, n_agents), 0, 3),
    "trust": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "punishment_willingness": np.clip(rng.normal(0.45, 0.18, n_agents), 0, 1),
    "process_fairness_weight": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
})

regime_params = {
    "fair_cooperative_regime": (0.50, 0.50, 0.40, 0.85),
    "unequal_but_cooperative_regime": (0.35, 0.65, 0.40, 0.70),
    "unequal_noncooperative_regime": (0.35, 0.65, -0.20, 0.45),
    "exploitative_low_process_fairness_regime": (0.25, 0.75, -0.35, 0.25),
}

def fairness_reciprocity_utility(
    self_payoff,
    other_payoff,
    fairness_sensitivity,
    reciprocity_sensitivity,
    reciprocity_signal,
    process_fairness,
    process_fairness_weight
):
    disadvantage_penalty = fairness_sensitivity * max(other_payoff - self_payoff, 0)
    reciprocity_component = reciprocity_sensitivity * reciprocity_signal
    process_component = process_fairness_weight * process_fairness
    return self_payoff - disadvantage_penalty + reciprocity_component + process_component

rows = []
for _, row in agents.iterrows():
    for period in range(1, periods + 1):
        post = int(period >= 3)
        regime = row["assigned_regime"] if post else "fair_cooperative_regime"
        self_payoff, other_payoff, reciprocity_signal, process_fairness = regime_params[regime]

        utility = fairness_reciprocity_utility(
            self_payoff,
            other_payoff,
            row["fairness_sensitivity"],
            row["reciprocity_sensitivity"],
            reciprocity_signal,
            process_fairness,
            row["process_fairness_weight"],
        )

        inequality_gap = max(other_payoff - self_payoff, 0)

        rejection_latent = (
            -0.5
            + 2.0 * row["fairness_sensitivity"] * inequality_gap
            - process_fairness
            - 0.4 * row["trust"]
            - 0.3 * reciprocity_signal
        )
        rejection_prob = 1 / (1 + np.exp(-rejection_latent))
        rejected = rng.binomial(1, rejection_prob)

        punishment_latent = (
            -0.8
            + 2.0 * row["punishment_willingness"]
            + 1.2 * inequality_gap
            - process_fairness
            - 0.2 * row["trust"]
        )
        punishment_prob = 1 / (1 + np.exp(-punishment_latent))
        punished = rng.binomial(1, punishment_prob) if rejected else 0

        cooperation_latent = (
            -0.2
            + 0.8 * row["trust"]
            + 0.9 * reciprocity_signal
            + 0.8 * process_fairness
            - 1.0 * inequality_gap
        )
        cooperation_prob = 1 / (1 + np.exp(-cooperation_latent))
        cooperated = rng.binomial(1, cooperation_prob)

        total_welfare = (
            utility
            + 0.25 * process_fairness
            + 0.15 * cooperated
            - 0.20 * rejected
            - 0.10 * punished
        )

        rows.append({
            "agent_id": int(row["agent_id"]),
            "period": period,
            "post": post,
            "regime": regime,
            "unequal_cooperative_treat": int(regime == "unequal_but_cooperative_regime"),
            "unequal_noncooperative_treat": int(regime == "unequal_noncooperative_regime"),
            "exploitative_low_process_treat": int(regime == "exploitative_low_process_fairness_regime"),
            "fairness_sensitivity": row["fairness_sensitivity"],
            "reciprocity_sensitivity": row["reciprocity_sensitivity"],
            "trust": row["trust"],
            "punishment_willingness": row["punishment_willingness"],
            "process_fairness_weight": row["process_fairness_weight"],
            "self_payoff": self_payoff,
            "other_payoff": other_payoff,
            "reciprocity_signal": reciprocity_signal,
            "process_fairness": process_fairness,
            "inequality_gap": inequality_gap,
            "fairness_reciprocity_utility": utility,
            "rejection_prob": rejection_prob,
            "rejected": rejected,
            "punishment_prob": punishment_prob,
            "punished": punished,
            "cooperation_prob": cooperation_prob,
            "cooperated": cooperated,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("agent_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_fairness_reciprocity_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_fairness_reciprocity_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_fairness_reciprocity_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_fairness_reciprocity_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows.")
print(f"Wrote {len(experiment):,} experiment rows.")
