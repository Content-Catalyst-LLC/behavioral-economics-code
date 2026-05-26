from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_anchoring_bias_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_anchoring_bias_panel.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_anchoring_bias_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_anchoring_bias_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_anchoring_bias_treatment_effects.csv").exists()

def test_anchoring_design_sensitivity_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "anchoring_design_sensitivity_analysis.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "anchoring_design_sensitivity.csv").exists()

def test_reference_price_simulation_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "reference_price_simulation.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "reference_price_simulation.csv").exists()
