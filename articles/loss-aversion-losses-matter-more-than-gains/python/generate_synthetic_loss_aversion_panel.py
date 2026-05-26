from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(24240)
n_agents = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n_agents),
    "alpha_gain": rng.uniform(0.75, 1.0, n_agents),
    "beta_loss": rng.uniform(0.75, 1.0, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "income_security": rng.uniform(0.10, 1.00, n_agents),
    "prior_loss_exposure": rng.binomial(1, 0.35, n_agents),
    "trust": rng.uniform(0.20, 1.00, n_agents),
})

def prospect_value(x, lam, alpha, beta):
    x_arr = np.asarray(x, dtype=float)
    return np.where(
        x_arr >= 0,
        x_arr ** alpha,
        -lam * ((-x_arr) ** beta),
    )

def simulate_frame(frame: str) -> pd.DataFrame:
    rows = []

    for _, row in agents.iterrows():
        lam = row["lambda_loss"]
        alpha = row["alpha_gain"]
        beta = row["beta_loss"]

        if frame == "gain":
            sure_value = prospect_value(200, lam, alpha, beta)
            risky_value = (
                (1 / 3) * prospect_value(600, lam, alpha, beta)
                + (2 / 3) * prospect_value(0, lam, alpha, beta)
            )
        elif frame == "loss":
            sure_value = prospect_value(-400, lam, alpha, beta)
            risky_value = (
                (2 / 3) * prospect_value(-600, lam, alpha, beta)
                + (1 / 3) * prospect_value(0, lam, alpha, beta)
            )
        elif frame == "mixed_gamble":
            sure_value = 0
            risky_value = (
                0.5 * prospect_value(240, lam, alpha, beta)
                + 0.5 * prospect_value(-100, lam, alpha, beta)
            )
        else:
            raise ValueError(f"Unknown frame: {frame}")

        rows.append({
            "agent_id": row["agent_id"],
            "frame": frame,
            "sure_value": float(sure_value),
            "risky_value": float(risky_value),
            "choose_risky": int(risky_value > sure_value),
        })

    return pd.DataFrame(rows)

panel = pd.concat([
    simulate_frame("gain"),
    simulate_frame("loss"),
    simulate_frame("mixed_gamble"),
], ignore_index=True)

panel = panel.merge(agents, on="agent_id", how="left")
panel["loss_frame_treat"] = (panel["frame"] == "loss").astype(int)
panel["mixed_gamble_treat"] = (panel["frame"] == "mixed_gamble").astype(int)

summary = panel.groupby("frame").agg(
    agents=("agent_id", "count"),
    share_choose_risky=("choose_risky", "mean"),
    mean_sure_value=("sure_value", "mean"),
    mean_risky_value=("risky_value", "mean"),
    mean_lambda=("lambda_loss", "mean"),
    mean_income_security=("income_security", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_loss_aversion_panel.csv", index=False)
summary.to_csv(TABLES / "loss_aversion_frame_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_loss_aversion_panel.csv", index=False)
summary.to_csv(PROCESSED / "loss_aversion_frame_summary.csv", index=False)

print(f"Wrote {len(panel):,} loss-aversion rows.")
print(summary)
