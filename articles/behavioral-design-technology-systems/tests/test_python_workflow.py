from pathlib import Path
import runpy


def test_python_workflow_runs():
    script = Path(__file__).resolve().parents[1] / "python" / "interface_regime_simulation.py"
    assert script.exists()
    runpy.run_path(str(script), run_name="__main__")
    output = Path(__file__).resolve().parents[1] / "outputs" / "tables" / "interface_regime_comparison.csv"
    assert output.exists()
