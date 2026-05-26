from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_bounded_rationality_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_bounded_rationality_panel.csv").exists()

def test_bounded_rationality_evaluation_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_bounded_rationality_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "bounded_rationality_constraint_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_bounded_rationality_estimates.csv").exists()

def test_administrative_burden_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "administrative_burden_simulation.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "administrative_burden_simulation.csv").exists()

def test_org_and_platform_examples_run():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "organizational_routine_policy_simplification_models.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "consumer_platform_search_friction_examples.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "organizational_routine_simulation.csv").exists()
    assert (root / "outputs" / "tables" / "consumer_platform_search_friction_examples.csv").exists()
