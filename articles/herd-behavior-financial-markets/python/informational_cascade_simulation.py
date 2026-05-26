from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(11112)

n_sequences = 500
sequence_length = 80

rows = []

for seq in range(1, n_sequences + 1):
    true_state = rng.choice([0, 1])
    public_buys = 0
    public_sells = 0

    for position in range(1, sequence_length + 1):
        private_signal_accuracy = 0.62
        private_signal = true_state if rng.random() < private_signal_accuracy else 1 - true_state

        social_signal = public_buys - public_sells
        private_component = 1 if private_signal == 1 else -1
        cascade_indicator = int(abs(social_signal) >= 3)

        decision_score = private_component + 0.45 * social_signal
        buy = int(decision_score > 0)

        if buy:
            public_buys += 1
        else:
            public_sells += 1

        rows.append({
            "sequence_id": seq,
            "position": position,
            "true_state": true_state,
            "private_signal": private_signal,
            "social_signal": social_signal,
            "cascade_indicator": cascade_indicator,
            "buy": buy,
            "decision_matches_private_signal": int(buy == private_signal),
            "decision_matches_true_state": int(buy == true_state),
            "public_buys": public_buys,
            "public_sells": public_sells,
        })

history = pd.DataFrame(rows)
summary = history.groupby("position").agg(
    cascade_rate=("cascade_indicator", "mean"),
    private_signal_disregard_rate=("decision_matches_private_signal", lambda x: 1 - x.mean()),
    accuracy_rate=("decision_matches_true_state", "mean"),
    buy_rate=("buy", "mean"),
).reset_index()

history.to_csv(TABLES / "informational_cascade_history.csv", index=False)
summary.to_csv(TABLES / "informational_cascade_position_summary.csv", index=False)

print(summary.tail())
