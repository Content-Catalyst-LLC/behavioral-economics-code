from pathlib import Path
import runpy


def test_synthetic_data_generator_runs():
    script = Path(__file__).resolve().parents[1] / "python" / "generate_synthetic_nudge_policy_panel.py"
    runpy.run_path(str(script), run_name="__main__")
    output = Path(__file__).resolve().parents[1] / "outputs" / "tables" / "synthetic_nudge_policy_experiment.csv"
    assert output.exists()


def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_nudge_policy_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_nudge_policy_evaluation.py"), run_name="__main__")
    output = root / "outputs" / "regression_tables" / "python_nudge_policy_treatment_effects.csv"
    assert output.exists()
