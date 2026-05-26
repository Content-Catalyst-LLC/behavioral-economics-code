from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(24241)

n_investors = 2500
assets_per_investor = 8

investors = pd.DataFrame({
    "investor_id": np.arange(1, n_investors + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n_investors),
    "trading_confidence": rng.uniform(0.20, 1.00, n_investors),
    "tax_sensitivity": rng.uniform(0.00, 0.50, n_investors),
    "liquidity_need": rng.uniform(0.00, 0.60, n_investors),
})

rows = []
for _, investor in investors.iterrows():
    for asset_id in range(1, assets_per_investor + 1):
        purchase_price = rng.uniform(20, 200)
        return_since_purchase = rng.normal(0.04, 0.22)
        current_price = max(1, purchase_price * (1 + return_since_purchase))
        paper_gain_loss = current_price - purchase_price
        winner = int(paper_gain_loss > 0)

        # Loss aversion reduces selling probability for losers; gain locking increases sale probability for winners.
        sale_score = (
            -0.75
            + 1.10 * winner
            - 0.75 * (1 - winner) * investor["lambda_loss"]
            + 0.45 * investor["liquidity_need"]
            + 0.25 * investor["trading_confidence"]
            + 0.20 * investor["tax_sensitivity"] * (1 - winner)
            + rng.normal(0, 0.35)
        )
        sale_probability = 1 / (1 + np.exp(-sale_score))
        sold = rng.binomial(1, sale_probability)

        rows.append({
            "investor_id": investor["investor_id"],
            "asset_id": asset_id,
            "lambda_loss": investor["lambda_loss"],
            "trading_confidence": investor["trading_confidence"],
            "tax_sensitivity": investor["tax_sensitivity"],
            "liquidity_need": investor["liquidity_need"],
            "purchase_price": purchase_price,
            "current_price": current_price,
            "paper_gain_loss": paper_gain_loss,
            "winner": winner,
            "sale_probability": sale_probability,
            "sold": sold,
        })

df = pd.DataFrame(rows)

summary = df.groupby("winner").agg(
    assets=("asset_id", "count"),
    sale_rate=("sold", "mean"),
    mean_paper_gain_loss=("paper_gain_loss", "mean"),
    mean_lambda=("lambda_loss", "mean"),
).reset_index()

df["lambda_quartile"] = pd.qcut(df["lambda_loss"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
het = df.groupby(["winner", "lambda_quartile"], observed=False).agg(
    assets=("asset_id", "count"),
    sale_rate=("sold", "mean"),
    mean_paper_gain_loss=("paper_gain_loss", "mean"),
    mean_lambda=("lambda_loss", "mean"),
).reset_index()

df.to_csv(TABLES / "disposition_effect_simulation.csv", index=False)
summary.to_csv(TABLES / "disposition_effect_summary.csv", index=False)
het.to_csv(TABLES / "disposition_effect_lambda_heterogeneity.csv", index=False)

print(summary)
print(het.head())
