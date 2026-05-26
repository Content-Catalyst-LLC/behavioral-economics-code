from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_trust_cooperation_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_trust_cooperation_experiment.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_trust_cooperation_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_trust_cooperation_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_trust_cooperation_treatment_effects.csv").exists()
