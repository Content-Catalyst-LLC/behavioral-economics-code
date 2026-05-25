from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from policy_microsimulation import evaluate_policy


def test_evaluate_policy_basic():
    df = pd.DataFrame(
        {
            "income": [50000, 80000],
            "environmental_concern": [0.5, 0.8],
            "present_bias": [0.3, 0.2],
            "loss_aversion": [2.0, 1.8],
            "norm_sensitivity": [0.4, 0.7],
            "friction_sensitivity": [0.5, 0.4],
            "quality_uncertainty": [0.3, 0.2],
            "infrastructure_access": [0.5, 0.8],
        }
    )
    out = evaluate_policy(df, subsidy=0.05, default_green=1, norm_signal=0.7, friction=0.08)
    assert "total_welfare" in out.columns
    assert out["adopted"].isin([0, 1]).all()
