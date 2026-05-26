from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(10011)
n_agents = 3000
n_rounds = 7000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "fairness_sensitivity": np.clip(rng.normal(1.2, 0.4, n_agents), 0, 3),
    "reciprocity_sensitivity": np.clip(rng.normal(1.0, 0.35, n_agents), 0, 3),
    "trust": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "punishment_willingness": np.clip(rng.normal(0.45, 0.18, n_agents), 0, 1),
    "process_fairness_weight": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
})

def utility_from_offer(offer_to_responder, fairness_sensitivity, process_fairness):
    responder_share = offer_to_responder
    proposer_share = 1 - offer_to_responder
    inequality_penalty = fairness_sensitivity * max(proposer_share - responder_share, 0)
    return responder_share - inequality_penalty + 0.25 * process_fairness

history = []
offers = np.round(np.arange(0.05, 1.00, 0.05), 2)

for round_id in range(1, n_rounds + 1):
    proposer_id, responder_id = rng.choice(agents["agent_id"], size=2, replace=False)
    proposer = agents.loc[agents["agent_id"] == proposer_id].iloc[0]
    responder = agents.loc[agents["agent_id"] == responder_id].iloc[0]
    process_fairness = rng.uniform(0.30, 0.90)

    proposer_scores = []
    for offer in offers:
        proposer_share = 1 - offer
        expected_acceptance = 1 / (1 + np.exp(-(5 * (offer - 0.30) - responder["fairness_sensitivity"] + responder["trust"] + process_fairness)))
        reciprocity_bonus = proposer["reciprocity_sensitivity"] * offer * process_fairness
        proposer_scores.append(proposer_share * expected_acceptance + 0.10 * reciprocity_bonus)

    chosen_offer = float(offers[int(np.argmax(proposer_scores))])
    responder_utility = utility_from_offer(chosen_offer, responder["fairness_sensitivity"], process_fairness)
    accepted = int(responder_utility >= 0)

    punishment_probability = 1 / (1 + np.exp(-(responder["punishment_willingness"] * 2.0 - chosen_offer * 4.0 - process_fairness)))
    punished = rng.binomial(1, punishment_probability) if not accepted else 0

    total_welfare = accepted * 1.0 - punished * 0.15 + process_fairness * 0.20 - abs(0.50 - chosen_offer) * 0.30

    history.append({
        "round": round_id,
        "proposer_id": int(proposer_id),
        "responder_id": int(responder_id),
        "offer_to_responder": chosen_offer,
        "proposer_share": 1 - chosen_offer,
        "accepted": accepted,
        "punished": punished,
        "process_fairness": process_fairness,
        "responder_utility": responder_utility,
        "total_welfare": total_welfare,
        "responder_fairness_sensitivity": responder["fairness_sensitivity"],
        "responder_reciprocity_sensitivity": responder["reciprocity_sensitivity"],
        "responder_trust": responder["trust"],
        "responder_punishment_willingness": responder["punishment_willingness"],
    })

bargaining = pd.DataFrame(history)
bargaining.to_csv(TABLES / "bargaining_punishment_history.csv", index=False)

summary = pd.DataFrame([{
    "mean_offer": bargaining["offer_to_responder"].mean(),
    "median_offer": bargaining["offer_to_responder"].median(),
    "acceptance_rate": bargaining["accepted"].mean(),
    "rejection_rate": 1 - bargaining["accepted"].mean(),
    "punishment_rate": bargaining["punished"].mean(),
    "mean_total_welfare": bargaining["total_welfare"].mean(),
}])
summary.to_csv(TABLES / "bargaining_punishment_summary.csv", index=False)

bargaining["fairness_quartile"] = pd.qcut(bargaining["responder_fairness_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
quartile_summary = bargaining.groupby("fairness_quartile", observed=False).agg(
    mean_offer=("offer_to_responder", "mean"),
    acceptance_rate=("accepted", "mean"),
    punishment_rate=("punished", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
).reset_index()
quartile_summary["rejection_rate"] = 1 - quartile_summary["acceptance_rate"]
quartile_summary.to_csv(TABLES / "bargaining_punishment_quartile_summary.csv", index=False)

print(summary)
print(quartile_summary)
