from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(22222)

n = 3500

agents = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "representativeness_sensitivity": rng.uniform(0.10, 0.90, n),
    "base_rate_attention": rng.uniform(0.10, 0.90, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "story_vividness": rng.uniform(0.20, 1.00, n),
})

true_base_rate = 0.18
story_consistency = rng.uniform(0.20, 1.00, n)

subjective_probability = np.clip(
    true_base_rate
    + agents["representativeness_sensitivity"].to_numpy() * story_consistency * agents["story_vividness"].to_numpy() * 0.28
    - agents["base_rate_attention"].to_numpy() * agents["numeracy"].to_numpy() * 0.12,
    0,
    1,
)

calibration_error = subjective_probability - true_base_rate
overestimation = (calibration_error > 0).astype(int)

df = agents.assign(
    true_base_rate=true_base_rate,
    story_consistency=story_consistency,
    subjective_probability=subjective_probability,
    calibration_error=calibration_error,
    overestimation=overestimation,
)

summary = df.groupby(pd.qcut(df["base_rate_attention"], 4, labels=["Q1", "Q2", "Q3", "Q4"]), observed=False).agg(
    agents=("agent_id", "count"),
    mean_subjective_probability=("subjective_probability", "mean"),
    mean_calibration_error=("calibration_error", "mean"),
    overestimation_rate=("overestimation", "mean"),
).reset_index().rename(columns={"base_rate_attention": "base_rate_attention_quartile"})

df.to_csv(TABLES / "base_rate_neglect_simulation.csv", index=False)
summary.to_csv(TABLES / "base_rate_neglect_summary.csv", index=False)

print(summary)
