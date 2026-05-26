from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_expected_utility_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_expected_utility_panel.csv").exists()

def test_expected_utility_evaluation_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_expected_utility_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "expected_utility_risk_aversion_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_expected_utility_estimates.csv").exists()

def test_certainty_equivalent_analysis_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_expected_utility_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "certainty_equivalent_risk_premium_analysis.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "certainty_equivalent_risk_premium_summary.csv").exists()

def test_insurance_portfolio_policy_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "insurance_portfolio_policy_risk_simulations.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "insurance_demand_simulation.csv").exists()
    assert (root / "outputs" / "tables" / "portfolio_choice_simulation.csv").exists()
    assert (root / "outputs" / "tables" / "expected_utility_policy_risk_example.csv").exists()
