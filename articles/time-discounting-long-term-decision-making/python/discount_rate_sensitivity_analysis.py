from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
for folder in [TABLES, DIAG]:
    folder.mkdir(parents=True, exist_ok=True)

future_values = [1_000_000, 10_000_000, 100_000_000]
horizons = [5, 10, 25, 50, 100]
discount_rates = [0.005, 0.01, 0.02, 0.03, 0.05, 0.07]

rows = []
for fv in future_values:
    for horizon in horizons:
        for rate in discount_rates:
            pv = fv / ((1 + rate) ** horizon)
            rows.append({
                "future_value": fv,
                "horizon_years": horizon,
                "discount_rate": rate,
                "present_value": pv,
                "pv_share_of_future_value": pv / fv,
            })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "discount_rate_sensitivity.csv", index=False)

climate_case = sensitivity[
    (sensitivity["future_value"] == 100_000_000)
    & (sensitivity["horizon_years"].isin([25, 50, 100]))
].copy()
climate_case.to_csv(DIAG / "long_horizon_public_goods_discount_sensitivity.csv", index=False)

print(sensitivity.head(20))
