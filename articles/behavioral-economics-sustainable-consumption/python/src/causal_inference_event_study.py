"""
Economist-grade causal inference scaffold.

Uses synthetic panel data to estimate a simple difference-in-differences model
and event-study style dynamic treatment profile. This is a demonstration scaffold,
not a validated empirical result.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "processed" / "synthetic_sustainable_consumption_panel.csv"
OUT_TABLES = ROOT / "outputs" / "tables"


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/src/generate_synthetic_microdata.py first."
        )

    df = pd.read_csv(DATA_PATH)

    did_model = smf.ols(
        "adopted ~ post_policy + C(household_id) + C(period)",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["locality_id"]})

    did_table = pd.DataFrame(
        {
            "term": did_model.params.index,
            "estimate": did_model.params.values,
            "std_error": did_model.bse.values,
            "p_value": did_model.pvalues.values,
        }
    )

    did_table.to_csv(OUT_TABLES / "did_policy_effect_summary.csv", index=False)

    # Event time relative to rollout. Never-treated localities are omitted from event-study dummy construction.
    treated = df[df["treated_locality"] == 1].copy()
    treated["event_time"] = treated["period"] - treated["policy_start_period"]

    # Use -1 as omitted baseline where available.
    event_times = sorted(t for t in treated["event_time"].unique() if -3 <= t <= 3 and t != -1)

    for t in event_times:
        treated[f"event_{t:+d}".replace("+", "plus").replace("-", "minus")] = (
            treated["event_time"] == t
        ).astype(int)

    event_terms = " + ".join(
        [f"event_{t:+d}".replace("+", "plus").replace("-", "minus") for t in event_times]
    )

    formula = f"adopted ~ {event_terms} + C(household_id) + C(period)"
    event_model = smf.ols(formula, data=treated).fit(
        cov_type="cluster", cov_kwds={"groups": treated["locality_id"]}
    )

    event_table = pd.DataFrame(
        {
            "term": event_model.params.index,
            "estimate": event_model.params.values,
            "std_error": event_model.bse.values,
            "p_value": event_model.pvalues.values,
        }
    )

    event_table.to_csv(OUT_TABLES / "event_study_dynamic_effects.csv", index=False)

    print("Difference-in-differences summary:")
    print(did_table[did_table["term"] == "post_policy"])
    print("Event-study terms:")
    print(event_table[event_table["term"].str.startswith("event_")])


if __name__ == "__main__":
    main()
