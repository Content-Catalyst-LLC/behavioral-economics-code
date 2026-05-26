from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_framing_effects_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_framing_effects_panel.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_framing_effects_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_framing_effects_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_framing_effects_treatment_effects.csv").exists()

def test_framing_design_sensitivity_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "framing_design_sensitivity_analysis.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "framing_design_sensitivity.csv").exists()
