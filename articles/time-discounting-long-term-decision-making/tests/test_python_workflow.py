from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_time_discounting_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_time_discounting_experiment.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_time_discounting_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_time_discounting_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_time_discounting_treatment_effects.csv").exists()

def test_discount_rate_sensitivity_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "discount_rate_sensitivity_analysis.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "discount_rate_sensitivity.csv").exists()
