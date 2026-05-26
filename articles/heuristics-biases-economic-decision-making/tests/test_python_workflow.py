from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_heuristics_biases_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_heuristics_biases_panel.csv").exists()

def test_policy_evaluation_runs_after_data_generation():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_heuristics_biases_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "causal_heuristics_biases_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_heuristics_biases_treatment_effects.csv").exists()

def test_design_sensitivity_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "heuristic_design_sensitivity_analysis.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "heuristic_design_sensitivity.csv").exists()

def test_base_rate_neglect_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "base_rate_neglect_simulation.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "base_rate_neglect_simulation.csv").exists()
