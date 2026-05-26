from pathlib import Path
import runpy

def test_synthetic_data_generator_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_loss_aversion_panel.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "synthetic_loss_aversion_panel.csv").exists()

def test_loss_aversion_evaluation_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "generate_synthetic_loss_aversion_panel.py"), run_name="__main__")
    runpy.run_path(str(root / "python" / "loss_aversion_frame_evaluation.py"), run_name="__main__")
    assert (root / "outputs" / "regression_tables" / "python_loss_aversion_frame_estimates.csv").exists()

def test_disposition_effect_runs():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "disposition_effect_simulation.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "disposition_effect_simulation.csv").exists()

def test_endowment_policy_models_run():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "python" / "endowment_consumer_policy_transition_models.py"), run_name="__main__")
    assert (root / "outputs" / "tables" / "endowment_effect_simulation.csv").exists()
    assert (root / "outputs" / "tables" / "policy_transition_loss_distribution.csv").exists()
