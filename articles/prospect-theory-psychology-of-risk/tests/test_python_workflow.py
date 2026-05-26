from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_prospect_theory_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_prospect_theory_panel.csv").exists()

def test_prospect_theory_evaluation_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_prospect_theory_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "prospect_theory_frame_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_prospect_theory_frame_estimates.csv").exists()

def test_expected_utility_comparison_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_prospect_theory_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "expected_utility_comparison.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "prospect_theory_expected_utility_comparison.csv").exists()

def test_fourfold_and_policy_examples_run():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "fourfold_risk_attitudes_simulation.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "insurance_lottery_policy_risk_examples.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "fourfold_risk_attitudes_simulation.csv").exists()
    assert (root / "outputs" / "tables" / "insurance_lottery_policy_risk_examples.csv").exists()
