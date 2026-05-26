from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(9091)
n_agents = 2500
n_rounds = 6000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "alpha": np.clip(rng.normal(1.5, 0.5, n_agents), 0, 3),
    "beta": np.clip(rng.normal(0.6, 0.3, n_agents), 0, 2),
    "income": np.exp(rng.normal(10.2, 0.55, n_agents)),
    "redistribution_norm": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "merit_belief": np.clip(rng.normal(0.50, 0.22, n_agents), 0, 1),
})

def fs_utility(self_payoff, other_payoff, alpha, beta):
    return self_payoff - alpha * max(other_payoff - self_payoff, 0) - beta * max(self_payoff - other_payoff, 0)

history = []
offers = np.round(np.arange(0.05, 1.00, 0.05), 2)

for round_id in range(1, n_rounds + 1):
    proposer_id, responder_id = rng.choice(agents["agent_id"], size=2, replace=False)
    proposer = agents.loc[agents["agent_id"] == proposer_id].iloc[0]
    responder = agents.loc[agents["agent_id"] == responder_id].iloc[0]

    proposer_utilities = [
        fs_utility(1 - offer, offer, proposer["alpha"], proposer["beta"])
        for offer in offers
    ]
    chosen_offer = float(offers[int(np.argmax(proposer_utilities))])

    responder_utility = fs_utility(
        chosen_offer,
        1 - chosen_offer,
        responder["alpha"],
        responder["beta"]
    )
    accepted = int(responder_utility >= 0)

    history.append({
        "round": round_id,
        "proposer_id": int(proposer_id),
        "responder_id": int(responder_id),
        "offer_to_responder": chosen_offer,
        "proposer_share": 1 - chosen_offer,
        "accepted": accepted,
        "responder_alpha": responder["alpha"],
        "responder_beta": responder["beta"],
        "proposer_alpha": proposer["alpha"],
        "proposer_beta": proposer["beta"],
        "responder_utility": responder_utility,
    })

bargaining = pd.DataFrame(history)
bargaining.to_csv(TABLES / "bargaining_history.csv", index=False)

summary = pd.DataFrame([{
    "mean_offer": bargaining["offer_to_responder"].mean(),
    "median_offer": bargaining["offer_to_responder"].median(),
    "acceptance_rate": bargaining["accepted"].mean(),
    "rejection_rate": 1 - bargaining["accepted"].mean(),
}])
summary.to_csv(TABLES / "bargaining_summary.csv", index=False)

redistribution_rows = []
for tau in np.arange(0, 0.50, 0.05):
    pre_tax = agents["income"].to_numpy()
    revenue = tau * pre_tax
    transfer = revenue.mean()
    post_tax = (1 - tau) * pre_tax + transfer
    mean_income = post_tax.mean()
    gap = np.abs(post_tax - mean_income) / mean_income

    social_utility = (
        post_tax
        - agents["alpha"].to_numpy() * np.maximum(mean_income - post_tax, 0) / mean_income
        - agents["beta"].to_numpy() * np.maximum(post_tax - mean_income, 0) / mean_income
        + agents["redistribution_norm"].to_numpy() * (1 - gap.mean())
        - agents["merit_belief"].to_numpy() * tau
    )

    redistribution_rows.append({
        "tax_rate": float(tau),
        "mean_post_tax_income": float(post_tax.mean()),
        "inequality_index": float(gap.mean()),
        "mean_social_preference_utility": float(social_utility.mean()),
        "support_share": float((social_utility > pre_tax).mean()),
    })

redistribution = pd.DataFrame(redistribution_rows)
redistribution.to_csv(TABLES / "redistribution_tax_rate_results.csv", index=False)

print(summary)
print(redistribution.sort_values("mean_social_preference_utility", ascending=False).head())
