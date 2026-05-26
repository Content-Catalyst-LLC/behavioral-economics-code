from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_framing_effects_panel.csv")

summary = df.groupby("frame").agg(
    agents=("agent_id", "count"),
    risky_choice_rate=("choose_risky", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
    mean_comprehension=("comprehension", "mean"),
    mean_loss_aversion=("loss_aversion", "mean"),
    mean_numeracy=("numeracy", "mean"),
    mean_trust=("trust", "mean"),
    mean_decision_fatigue=("decision_fatigue", "mean"),
    mean_frame_strength=("frame_strength", "mean"),
    mean_disclosure_quality=("disclosure_quality", "mean"),
    mean_salience=("salience", "mean"),
).reset_index()

summary["welfare_per_risky_choice_point"] = summary["mean_welfare_proxy"] / summary["risky_choice_rate"].replace(0, float("nan"))
summary.to_csv(TABLES / "framing_comprehension_welfare_summary.csv", index=False)

rows = []
for comprehension_weight in [0.75, 1.00, 1.25]:
    for autonomy_weight in [0.75, 1.00, 1.25]:
        for manipulation_penalty in [0.75, 1.00, 1.25]:
            alt_welfare = (
                df["welfare_proxy"]
                + comprehension_weight * df["comprehension"] * 10
                + autonomy_weight * df["disclosure_quality"] * df["numeracy"] * 5
                - manipulation_penalty * df["frame_strength"] * df["salience"] * (1 - df["comprehension"]) * 8
            )
            tmp = df.assign(alt_welfare=alt_welfare)
            for frame, sub in tmp.groupby("frame"):
                rows.append({
                    "comprehension_weight": comprehension_weight,
                    "autonomy_weight": autonomy_weight,
                    "manipulation_penalty": manipulation_penalty,
                    "frame": frame,
                    "mean_alt_welfare": sub["alt_welfare"].mean(),
                    "median_alt_welfare": sub["alt_welfare"].median(),
                })

pd.DataFrame(rows).to_csv(DIAG / "framing_welfare_sensitivity.csv", index=False)

print(summary)
