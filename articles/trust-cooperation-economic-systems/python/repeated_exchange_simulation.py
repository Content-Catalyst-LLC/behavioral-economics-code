from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(8081)
n_agents = 1000
rounds = 50

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "trust_propensity": np.clip(rng.normal(0.55, 0.18, n_agents), 0, 1),
    "reciprocity": np.clip(rng.normal(0.50, 0.20, n_agents), 0, 1),
    "punishment_willingness": np.clip(rng.normal(0.40, 0.18, n_agents), 0, 1),
    "institutional_trust": np.clip(rng.normal(0.55, 0.20, n_agents), 0, 1),
    "betrayal_sensitivity": np.clip(rng.normal(0.60, 0.16, n_agents), 0, 1),
})

rows = []
for round_id in range(1, rounds + 1):
    institutional_support = 0.35 if round_id <= 20 else 0.70
    norm_strength = 0.40 if round_id <= 20 else 0.70
    punishment_credibility = 0.35 if round_id <= 20 else 0.65

    shuffled = rng.permutation(agents["agent_id"].to_numpy())
    pairs = shuffled.reshape(-1, 2)

    for sender_id, receiver_id in pairs:
        sender = agents.loc[agents["agent_id"] == sender_id].iloc[0]
        receiver = agents.loc[agents["agent_id"] == receiver_id].iloc[0]
        send_prob = 1 / (1 + np.exp(-(1.6 * sender["trust_propensity"] + 0.8 * sender["institutional_trust"] * institutional_support + 0.6 * norm_strength - 0.7 * sender["betrayal_sensitivity"])))
        sent = rng.binomial(1, send_prob)
        return_prob = 1 / (1 + np.exp(-(1.8 * receiver["reciprocity"] + 0.7 * norm_strength + 0.5 * institutional_support - 0.4)))
        returned = rng.binomial(1, return_prob) if sent else 0
        punish_prob = 1 / (1 + np.exp(-(1.7 * sender["punishment_willingness"] + 0.8 * punishment_credibility - 0.8)))
        punished = rng.binomial(1, punish_prob) if sent and not returned else 0
        sender_welfare = sent * (0.80 * returned - 0.70 * (1 - returned)) - 0.15 * punished + 0.20 * institutional_support
        receiver_welfare = sent * (0.50 + 0.30 * returned - 0.20 * punished)

        rows.append({
            "round": round_id,
            "sender_id": int(sender_id),
            "receiver_id": int(receiver_id),
            "sent": sent,
            "returned": returned,
            "punished": punished,
            "institutional_support": institutional_support,
            "norm_strength": norm_strength,
            "punishment_credibility": punishment_credibility,
            "sender_welfare": sender_welfare,
            "receiver_welfare": receiver_welfare,
            "total_welfare": sender_welfare + receiver_welfare,
        })

history = pd.DataFrame(rows)
summary = history.groupby("round").agg(
    trust_rate=("sent", "mean"),
    reciprocity_rate=("returned", "mean"),
    punishment_rate=("punished", "mean"),
    mean_total_welfare=("total_welfare", "mean"),
    institutional_support=("institutional_support", "mean"),
    norm_strength=("norm_strength", "mean"),
    punishment_credibility=("punishment_credibility", "mean"),
).reset_index()

history.to_csv(TABLES / "repeated_exchange_history.csv", index=False)
summary.to_csv(TABLES / "repeated_exchange_round_summary.csv", index=False)
print(summary.tail())
