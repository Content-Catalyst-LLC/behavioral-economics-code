from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_fairness_reciprocity_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_fairness_reciprocity_experiment.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_fairness_reciprocity_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_fairness_reciprocity_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_fairness_reciprocity_treatment_effects.csv").exists()
