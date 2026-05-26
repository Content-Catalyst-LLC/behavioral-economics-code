from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(19190)

n_agents = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "loss_aversion": rng.uniform(1.0, 3.0, n_agents),
    "curvature": rng.uniform(0.70, 1.00, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "trust": rng.uniform(0.20, 1.00, n_agents),
    "decision_fatigue": rng.uniform(0.00, 0.40, n_agents),
})

def prospect_value(x: np.ndarray | float, lam: float, eta: float) -> np.ndarray:
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** eta, -lam * ((-x_arr) ** eta))

def simulate_frame(
    frame_name: str,
    frame_strength: float,
    disclosure_quality: float,
    salience: float,
) -> pd.DataFrame:
    if frame_name == "gain_frame":
        certain_outcome = 200
        risky_values = np.array([600, 0])
        risky_probabilities = np.array([1/3, 2/3])
    elif frame_name == "loss_frame":
        certain_outcome = -400
        risky_values = np.array([-600, 0])
        risky_probabilities = np.array([2/3, 1/3])
    elif frame_name == "balanced_absolute_risk_frame":
        certain_outcome = 200
        risky_values = np.array([600, 0])
        risky_probabilities = np.array([1/3, 2/3])
    else:
        raise ValueError(f"Unknown frame: {frame_name}")

    rows = []
    for _, row in agents.iterrows():
        lam = row["loss_aversion"]
        eta = row["curvature"]

        certain_value = float(prospect_value(certain_outcome, lam, eta))
        risky_value = float(np.sum(risky_probabilities * prospect_value(risky_values, lam, eta)))

        comprehension = np.clip(
            disclosure_quality * row["numeracy"]
            + 0.20 * row["trust"]
            - 0.25 * row["decision_fatigue"],
            0,
            1,
        )

        if frame_name == "gain_frame":
            framing_shift = -frame_strength * salience * 20
        elif frame_name == "loss_frame":
            framing_shift = frame_strength * salience * lam * 22
        else:
            framing_shift = 0.05 * salience * 5

        adjusted_risky_value = risky_value + framing_shift + comprehension * 5
        choose_risky = int(adjusted_risky_value >= certain_value)

        welfare_proxy = (
            risky_value if choose_risky == 1 else certain_value
        ) + comprehension * 10 - row["decision_fatigue"] * 5

        rows.append({
            "agent_id": int(row["agent_id"]),
            "frame": frame_name,
            "loss_aversion": row["loss_aversion"],
            "curvature": row["curvature"],
            "numeracy": row["numeracy"],
            "trust": row["trust"],
            "decision_fatigue": row["decision_fatigue"],
            "certain_value": certain_value,
            "risky_value": risky_value,
            "adjusted_risky_value": adjusted_risky_value,
            "comprehension": comprehension,
            "choose_risky": choose_risky,
            "welfare_proxy": welfare_proxy,
            "frame_strength": frame_strength,
            "disclosure_quality": disclosure_quality,
            "salience": salience,
            "loss_frame_treat": int(frame_name == "loss_frame"),
            "balanced_frame_treat": int(frame_name == "balanced_absolute_risk_frame"),
        })

    return pd.DataFrame(rows)

panel = pd.concat([
    simulate_frame("gain_frame", frame_strength=0.70, disclosure_quality=0.70, salience=0.75),
    simulate_frame("loss_frame", frame_strength=0.70, disclosure_quality=0.70, salience=0.75),
    simulate_frame("balanced_absolute_risk_frame", frame_strength=0.15, disclosure_quality=0.95, salience=0.35),
], ignore_index=True)

summary = panel.groupby("frame").agg(
    agents=("agent_id", "count"),
    risky_choice_rate=("choose_risky", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
    mean_comprehension=("comprehension", "mean"),
    mean_adjusted_risky_value=("adjusted_risky_value", "mean"),
    mean_loss_aversion=("loss_aversion", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_framing_effects_panel.csv", index=False)
summary.to_csv(TABLES / "framing_effects_frame_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_framing_effects_panel.csv", index=False)
summary.to_csv(PROCESSED / "framing_effects_frame_summary.csv", index=False)

print(f"Wrote {len(panel):,} framing-regime rows.")
print(summary)
