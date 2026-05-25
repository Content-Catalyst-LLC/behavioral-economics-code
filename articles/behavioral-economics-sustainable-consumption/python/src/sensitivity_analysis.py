"""
Sensitivity analysis for behavioral parameters.

This script varies loss aversion, present bias, norm sensitivity, and friction
to show how policy rankings can change under alternative behavioral assumptions.
"""

from __future__ import annotations

from pathlib import Path
import itertools
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "synthetic" / "synthetic_households.csv"
OUT_TABLES = ROOT / "outputs" / "tables"


def score_adoption(df: pd.DataFrame, loss_scale: float, present_scale: float, norm_scale: float, friction_scale: float) -> float:
    utility_diff = (
        -0.55
        + 1.05 * df["environmental_concern"]
        + norm_scale * 0.70 * df["norm_sensitivity"] * 0.70
        + 0.60
        + 0.40 * df["infrastructure_access"]
        - loss_scale * 0.18 * df["loss_aversion"]
        - present_scale * 0.20 * df["present_bias"]
        - friction_scale * 0.12 * df["friction_sensitivity"]
        - 0.45 * df["quality_uncertainty"]
    )
    return float((1 / (1 + np.exp(-utility_diff))).mean())


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    grid = {
        "loss_scale": [0.75, 1.00, 1.25, 1.50],
        "present_scale": [0.75, 1.00, 1.25, 1.50],
        "norm_scale": [0.75, 1.00, 1.25, 1.50],
        "friction_scale": [0.75, 1.00, 1.25, 1.50],
    }

    rows = []
    for loss_scale, present_scale, norm_scale, friction_scale in itertools.product(*grid.values()):
        rows.append(
            {
                "loss_scale": loss_scale,
                "present_scale": present_scale,
                "norm_scale": norm_scale,
                "friction_scale": friction_scale,
                "mean_adoption_probability": score_adoption(
                    df, loss_scale, present_scale, norm_scale, friction_scale
                ),
            }
        )

    out = pd.DataFrame(rows).sort_values("mean_adoption_probability", ascending=False)
    out.to_csv(OUT_TABLES / "behavioral_parameter_sensitivity.csv", index=False)
    print(out.head(12))
    print(out.tail(12))


if __name__ == "__main__":
    main()
