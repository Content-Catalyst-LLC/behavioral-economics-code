from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(9090)
n_agents = 9000
periods = 4

regimes = np.array([
    "equal_distribution",
    "advantageous_inequality",
    "disadvantageous_inequality",
])

assigned = rng.choice(regimes, size=n_agents, p=[0.34, 0.33, 0.33])

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "assigned_regime": assigned,
    "alpha": np.clip(rng.normal(1.5, 0.5, n_agents), 0, 3),
    "beta": np.clip(rng.normal(0.6, 0.3, n_agents), 0, 2),
    "income": np.exp(rng.normal(10.2, 0.55, n_agents)),
    "redistribution_norm": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "merit_belief": np.clip(rng.normal(0.50, 0.22, n_agents), 0, 1),
    "institutional_trust": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "process_fairness_sensitivity": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
})

payoffs = {
    "equal_distribution": (0.50, 0.50, 0.75),
    "advantageous_inequality": (0.70, 0.30, 0.48),
    "disadvantageous_inequality": (0.30, 0.70, 0.42),
}

def fehr_schmidt_utility(self_payoff, other_payoff, alpha, beta):
    return (
        self_payoff
        - alpha * max(other_payoff - self_payoff, 0)
        - beta * max(self_payoff - other_payoff, 0)
    )

rows = []
for _, row in agents.iterrows():
    for period in range(1, periods + 1):
        post = int(period >= 3)
        regime = row["assigned_regime"] if post else "equal_distribution"
        self_payoff, other_payoff, baseline_legitimacy = payoffs[regime]

        social_preference_utility = fehr_schmidt_utility(
            self_payoff,
            other_payoff,
            row["alpha"],
            row["beta"]
        )

        inequality_gap = abs(self_payoff - other_payoff)

        process_legitimacy = np.clip(
            baseline_legitimacy
            + 0.15 * row["institutional_trust"]
            - 0.20 * inequality_gap
            + 0.10 * row["merit_belief"] * (regime == "advantageous_inequality")
            - 0.10 * row["alpha"] * (regime == "disadvantageous_inequality") / 3,
            0,
            1
        )

        rejection_latent = (
            -0.4
            + 1.3 * row["alpha"] * max(other_payoff - self_payoff, 0)
            + 0.7 * row["beta"] * max(self_payoff - other_payoff, 0)
            - 0.8 * process_legitimacy
            - 0.3 * row["institutional_trust"]
        )

        rejection_prob = 1 / (1 + np.exp(-rejection_latent))
        rejected = rng.binomial(1, rejection_prob)

        redistribution_latent = (
            -0.2
            + 0.8 * row["redistribution_norm"]
            + 0.5 * row["alpha"]
            - 0.6 * row["merit_belief"]
            + 0.3 * row["institutional_trust"]
            + 0.4 * inequality_gap
        )

        redistribution_support_prob = 1 / (1 + np.exp(-redistribution_latent))
        support_redistribution = rng.binomial(1, redistribution_support_prob)

        total_welfare = (
            self_payoff
            + social_preference_utility
            + 0.35 * process_legitimacy
            + 0.10 * support_redistribution
            - 0.20 * rejected
        )

        rows.append({
            "agent_id": int(row["agent_id"]),
            "period": period,
            "post": post,
            "regime": regime,
            "advantageous_treat": int(regime == "advantageous_inequality"),
            "disadvantageous_treat": int(regime == "disadvantageous_inequality"),
            "alpha": row["alpha"],
            "beta": row["beta"],
            "income": row["income"],
            "redistribution_norm": row["redistribution_norm"],
            "merit_belief": row["merit_belief"],
            "institutional_trust": row["institutional_trust"],
            "process_fairness_sensitivity": row["process_fairness_sensitivity"],
            "self_payoff": self_payoff,
            "other_payoff": other_payoff,
            "inequality_gap": inequality_gap,
            "process_legitimacy": process_legitimacy,
            "social_preference_utility": social_preference_utility,
            "rejection_prob": rejection_prob,
            "rejected": rejected,
            "redistribution_support_prob": redistribution_support_prob,
            "support_redistribution": support_redistribution,
            "total_welfare": total_welfare,
        })

panel = pd.DataFrame(rows)
experiment = panel.loc[panel["post"] == 1].groupby("agent_id", as_index=False).tail(1)

panel.to_csv(TABLES / "synthetic_inequality_aversion_panel.csv", index=False)
experiment.to_csv(TABLES / "synthetic_inequality_aversion_experiment.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_inequality_aversion_panel.csv", index=False)
experiment.to_csv(PROCESSED / "synthetic_inequality_aversion_experiment.csv", index=False)

print(f"Wrote {len(panel):,} panel rows.")
print(f"Wrote {len(experiment):,} experiment rows.")
